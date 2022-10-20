#!/usr/bin/env python3
import argparse
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

for performance in ["hIndex", "paperCount", "citationCount"]:
    cited_author_pos = []
    cited_author_perf = []
    nocited_author_perf = []
    author_perf = []
    print(performance)
    for paper in data:
        ref_authors = set([x for r in paper["references"] for x in r["authors"]])

        authors_perf_local = [(x[performance], x["name"]) for x in paper["authors"] if x[performance]]
        cited_author_perf += [a[0] for a in authors_perf_local if a[1] in ref_authors]
        nocited_author_perf += [a[0] for a in authors_perf_local if a[1] not in ref_authors]
        author_perf += [a[0] for a in authors_perf_local]

    print(f"Avg. perf: {np.average(author_perf):.1f}")
    print(f"Avg. self-cited perf: {np.average(cited_author_perf):.1f}")
    print(f"Avg. no self-cited perf: {np.average(nocited_author_perf):.1f}")
    print(f"Avg. diff: {np.average(cited_author_perf)-np.average(nocited_author_perf):.1f}")
    print()