#!/usr/bin/env python3
import argparse
import json
import numpy as np

# RQ3: What are the properties of self-cited papers?

args = argparse.ArgumentParser()
args.add_argument(
    "-d", "--data", default="data/acl_w_references.jsonl",
)
args = args.parse_args()

with open(args.data, "r") as f:
    data = [json.loads(x) for x in f.readlines()]

for performance in ["year", "citationCount"]:
    cited_perf = []
    nocited_perf = []
    print(performance)
    for paper in data:
        authors = set([x["name"] for x in paper["authors"]])
        references = [(r[performance], len(authors.intersection(set(r["authors"]))) != 0) for r in paper["references"] if r[performance] is not None]

        if performance == "year":
            references = [(paper["year"] - r[0], r[1]) for r in references]
        cited_perf += [r[0] for r in references if r[1]]
        nocited_perf += [r[0] for r in references if not r[1]]

    print(f"Avg. self-cited perf: {np.average(cited_perf):.0f}")
    print(f"Avg. no self-cited perf: {np.average(nocited_perf):.0f}")
    print(f"Avg. diff: {np.average(cited_perf)-np.average(nocited_perf):.0f}")
    print()