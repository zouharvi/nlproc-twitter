#!/usr/bin/env python3
import argparse
from collections import defaultdict
import copy
import json
import numpy as np
import matplotlib.pyplot as plt
import fig_utils

# Is self-citation dependent on author popularity? (paper count, citation count, hindex)

args = argparse.ArgumentParser()
args.add_argument(
    "-d", "--data", default="data/acl_w_references.jsonl",
)
args = args.parse_args()

with open(args.data, "r") as f:
    data = [json.loads(x) for x in f.readlines()]

author_to_author = defaultdict(lambda: defaultdict(int))

for paper in data:
    authors = [x["name"] for x in paper["authors"]]
    for author in authors:
        for reference in paper["references"]:
            for r_author in reference["authors"]:
                author_to_author[author][r_author] += 1

author_to_author_score = []
author_to_author_copy = copy.deepcopy(author_to_author)

for author, cited_authors in author_to_author.items():
    for r_author in cited_authors:
        cited_to = cited_authors[r_author]
        cited_from = author_to_author_copy[r_author][author]
        author_to_author_score.append((author, r_author, cited_to, cited_from))

i = 0
author_to_author_score.sort(key=lambda x: x[2]+x[3], reverse=True)
printed = set()
while i < 40:
    i += 1
    author, r_author, cited_to, cited_from = author_to_author_score.pop(0)
    if (author, r_author) in printed:
        continue
    printed.add((author, r_author))
    rest = f"and reverse {cited_from}"
    if author == r_author:
        r_author = "themselves"
        rest = ""

    print(f"{author:>25} cited {r_author:<25} {cited_to:<3} times {rest}")


self_favourite = []
for author, cited_authors in author_to_author.items():
    cited_authors = sorted(list(cited_authors.items()), key=lambda x: x[1], reverse=True)
    favourite_author = cited_authors[0]
    if favourite_author[1] < 2:
        continue
    self_favourite.append(favourite_author[0] == author)
print(f"People who's favourite author is themselves: {np.average(self_favourite):.2%}")