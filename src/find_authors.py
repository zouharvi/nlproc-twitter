#!/usr/bin/env python3

from twitter import *
from keys import *
import argparse
import bibtexparser
import re
import tqdm
import random
import semanticscholar

args = argparse.ArgumentParser()
args.add_argument("-b", "--bib", default=None)
args.add_argument("-a", "--arxiv", default=None)
args.add_argument("-s", "--s2", default=None)
args = args.parse_args()

BIBLATEX_FIX = [
    ("\\'e", "é"), ("\\'a", "á"),
    ("\\vs", "š"), ("\\vr", "ř"),
    ("\\'c", "ć"), ('\\"a', "ä"),
    ("\\vz", "ž"), ("\\'u", "ú"),
]

t = Twitter(
    auth=OAuth(
        token=ACCESS_TOKEN, token_secret=ACCESS_TOKEN_SECRET,
        consumer_key=API_KEY, consumer_secret=API_KEY_SECRET
    ),
    retry=True,
)

if not args.bib and not args.arxiv and not args.s2:
    print("Either bibfile, arXiv link or SemanticScholar link need to be specified")
    exit()

authors_out = set()

if args.bib:
    re_whitespace = re.compile(r'\s+')
    re_escape = re.compile(r'\\.')
    re_nonalpha = re.compile(r'[^\w]')
    with open(args.bib) as f:
        bib_data = bibtexparser.load(f)
    for bib_entry in bib_data.entries:
        authors = bib_entry["author"].replace("\n", " ").lower()
        authors = authors.replace("{", "").replace("}", "")
        for fix in BIBLATEX_FIX:
            authors = authors.replace(*fix)

        # remove unfixed escapes
        authors = re_escape.sub(' ', authors)
        # remove non-letter characters
        authors = re_nonalpha.sub(' ', authors)
        # collapse whitespace and split
        authors = re_whitespace.sub(' ', authors).split(" and ")

        for author in authors:
            author = author.strip()
            if author in {"others", "other"}:
                continue
            author = author.split(" ")
            author_first = author[0]
            author_rest = " ".join(author[1:])
            authors_out.add(author_rest + " " + author_first)
elif args.arxiv or args.s2:
    sch = semanticscholar.SemanticScholar()
    if args.arxiv:
        # take only the last part
        arxiv_id = args.arxiv.split("/")[-1]
        arxiv_id = arxiv_id.rstrip(".pdf")
        paper = sch.get_paper(f"arxiv:{arxiv_id}")
    elif args.s2:
        # take only the last part
        paper_id = args.s2.split("/")[-1]
        paper = sch.get_paper(paper_id)
    else:
        raise Exception("Logic error")
    if not dict(paper):
        print("Unable to find the paper via S2 API")
        exit()
    for reference in paper["references"]:
        reference_authors = [x["name"] for x in reference["authors"]]
        authors_out |= set(reference_authors)

authors_out = sorted(authors_out)
random.seed(0)
random.shuffle(authors_out)

print(f"The given paper cites {len(authors_out)} authors in total")

for author in tqdm.tqdm(authors_out):
    results = t.users.search(q=author, count=10, page=0)
    hit = False

    if len(results) > 5:
        print("Too many results, skipping", author)
        continue

    for user in results:
        # some basic heuristics
        if user["following"]:
            continue
        if len(user['description']) == 0:
            continue
        if user["followers_count"] < 50:
            continue

        print("\nLooking for", " " * 30, author)
        twitter_url = f"https://www.twitter.com/{user['screen_name']}"
        print(f"{twitter_url:<40}  ({user['name']})")
        print(
            "Following/followers:", " " * 21,
            f'{user["friends_count"]} / {user["followers_count"]}'
        )
        print(
            "Description:        ", " " * 21,
            user['description'].replace("\n", "\\n")
        )
        hit = True

    if hit:
        input()
