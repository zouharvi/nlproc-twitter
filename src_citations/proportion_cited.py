#!/usr/bin/env python3
import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import fig_utils

# - RQ1: What is the proportion of paper authors which are cited?
#   - What is the number of distinct self-citations?

args = argparse.ArgumentParser()
args.add_argument(
    "-d", "--data", default="data/acl_w_references.jsonl",
)
args = args.parse_args()

with open(args.data, "r") as f:
    data = [json.loads(x) for x in f.readlines()]

perc_cited = []
dist_citations = []
for paper in data:
    authors = set([x["name"] for x in paper["authors"]])
    ref_authors = set([x for r in paper["references"] for x in r["authors"]])
    proportion = len(authors.intersection(ref_authors)) / len(authors)
    perc_cited.append(proportion)

    ref_authors_nonflat = [set(r["authors"]) for r in paper["references"]]
    dist_citations.append(len([r for r in ref_authors_nonflat if len(authors.intersection(r)) != 0]))
    

print(f"Not cited at all: {len([x for x in perc_cited if x == 0])/len(perc_cited):.0%}")
print(f"All cited: {len([x for x in perc_cited if x == 1])/len(perc_cited):.0%}")
print(f"Avg. proportion cited if cited: {np.average([x for x in perc_cited if x != 0]):.1f}")
print(f"Number of distinct citations: {np.average(dist_citations):.1f}")

fig = plt.figure(figsize=(5,3))
ax = plt.gca()
perc_cited = sorted(perc_cited)
plt.scatter(
    range(len(perc_cited)),
    perc_cited,
    alpha=0.3,
    s=15,
    color=fig_utils.COLOR1,
)
plt.hlines(
    np.average(perc_cited), xmin=0, xmax=len(perc_cited),
    color=fig_utils.COLOR2, linestyle=":"
)
plt.text(
    0, 0.54, f"$\mu = {np.average(perc_cited):.2f}$",
    color="black",
)
plt.ylabel("Proportion of authors cited")
plt.xlabel("Papers (sorted)")
ax.axes.xaxis.set_ticklabels([])
plt.tight_layout()
plt.savefig("figures/proportion_cited.png", dpi=200)
plt.show()