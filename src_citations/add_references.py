#!/usr/bin/env python3

import json
import sys
import time
sys.path.append("src")
sys.path.append("src_citations")
import keys
import semanticscholar
import pandas as pd
import tqdm
import argparse
import urllib.request

def paper_references(paper_id, limit=200):
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references?fields=title,authors,year,citationCount&limit={limit}"
    print(url)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
        "x-api-key": keys.S2_API_KEY
    }
    request = urllib.request.Request(url, headers=header)
    data = urllib.request.urlopen(request)
    data = data.read().decode("utf-8")
    return json.loads(data)["data"]

def paper_authors(paper_id, limit=200):
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/authors?fields=name,paperCount,citationCount,hIndex&limit={limit}"
    print(url)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
        "x-api-key": keys.S2_API_KEY
    }
    request = urllib.request.Request(url, headers=header)
    data = urllib.request.urlopen(request)
    data = data.read().decode("utf-8")
    return json.loads(data)["data"]

def paper_main(paper_id, limit=200):
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=citationCount,authors,year,publicationTypes&limit={limit}"
    print(url)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
        "x-api-key": keys.S2_API_KEY
    }
    request = urllib.request.Request(url, headers=header)
    data = urllib.request.urlopen(request)
    data = data.read().decode("utf-8")
    return json.loads(data)

s2 = semanticscholar.SemanticScholar(api_key=keys.S2_API_KEY)

args = argparse.ArgumentParser()
args.add_argument(
    "-d", "--data", default="data/acl-publication-info.74k.parquet",
    help="Path to the input parquet file."
)
args.add_argument(
    "-o", "--output", default="data/acl_w_references.jsonl",
    help="Path to the output jsonl file."
)
args.add_argument(
    "-t", "--total", type=int, default=None,
    help="How many rows to consider (for fast development)."
)
args = args.parse_args()
data = pd.read_parquet(args.data)

# clear file
f = open(args.output, "a")

data = data[1216+634:]


for row_i, row in tqdm.tqdm(
    data[:args.total].iterrows(),
    total=args.total if args.total is not None else data.shape[0]
):
    try:
        # if any row has title/abstract/full_text empty, consider it invalid
        if len(row["title"].strip()) == 0 or len(row["abstract"].strip()) == 0 or len(row["full_text"].strip()) == 0:
            continue

        references = paper_references("ACL:" + row["acl_id"])
        references = [
            {
                "authors": [a["name"] for a in r["citedPaper"]["authors"]],
                "year": r["citedPaper"]["year"],
                "citationCount": r["citedPaper"]["citationCount"],
            }
            for r in references
        ]
        authors = paper_authors("ACL:" + row["acl_id"])

        paper = paper_main("ACL:" + row["acl_id"])

        lineout = {
            "acl_id": row["acl_id"],
            "title": row["title"],
            "authors": authors,
            "year": paper["year"],
            "publicationTypes": paper["publicationTypes"],
            "citationCount": paper["citationCount"],
            "references": references
        }
        f.write(json.dumps(lineout, ensure_ascii=False) + "\n")

        # throttle
        # time.sleep(0.5)
    except Exception as e:
        print(e)