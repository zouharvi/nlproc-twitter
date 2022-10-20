#!/usr/bin/env python3
import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import fig_utils

# - RQ2: Which author cites themselves the most? (include none, normalize wrt length?)
#  - Is self-citation dependent on author popularity? (paper count, citation count, hindex)

args = argparse.ArgumentParser()
args.add_argument(
    "-d", "--data", default="data/acl_w_references.jsonl",
)
args = args.parse_args()

with open(args.data, "r") as f:
    data = [json.loads(x) for x in f.readlines()]

cited_author_pos = []
for paper in data:
    authors = [x["name"] for x in paper["authors"]]
    ref_authors = set([x for r in paper["references"] for x in r["authors"]])
    cited_author_pos.append([a_i/len(authors) for a_i, a in enumerate(authors) if a in ref_authors])

print(f"Avg. position: {np.average([x for r in cited_author_pos for x in r]):.1f}")

fig = plt.figure(figsize=(5,3))
ax = plt.gca()
cited_author_pos = sorted([x for r in cited_author_pos for x in r])
plt.scatter(
    range(len(cited_author_pos)),
    cited_author_pos,
    alpha=0.3,
    s=15,
    color=fig_utils.COLOR1,
)
plt.hlines(
    np.average(cited_author_pos), xmin=0, xmax=len(cited_author_pos),
    color=fig_utils.COLOR2, linestyle=":"
)
plt.text(
    0, 0.4, f"$\mu = {np.average(cited_author_pos):.2f}$",
    color="black",
)
plt.ylabel("Self-cited author position")
plt.xlabel("Papers (sorted)")
plt.yticks([0, 1], ["First", "Last"])
ax.axes.xaxis.set_ticklabels([])
plt.tight_layout()
plt.savefig("figures/author_position.png", dpi=200)
plt.show()