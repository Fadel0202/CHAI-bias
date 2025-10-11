from penman import load
from penman import load
import matplotlib.pyplot as plt
from collections import Counter

import logging

from src.config import cfg 

logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("penman").setLevel(logging.ERROR)
logging.getLogger("penman.codec").setLevel(logging.ERROR)

amr_file = cfg.amr_path

with open(amr_file, "r", encoding="utf-8") as f:
    amr_graphs = list(load(f))

# Extract concepts containing "bias"
bias_concepts = set()

for graph in amr_graphs:
    for triple in graph.triples:
        # triple = (source, relation, target)
        if triple[1] == ':instance' and triple[2] and 'bias' in triple[2].lower():
            bias_concepts.add(triple[2].lower())

bias_concepts = sorted(bias_concepts)
print(f"Concepts related to 'bias' in AMR: {bias_concepts}")


def analyze_bias_structure(graph):
    """Return structure info for nodes related to bias or bias-01."""
    triples = graph.triples
    bias_nodes = [
        src
        for (src, rel, tgt) in triples
        if rel == ':instance' and tgt and 'bias' in tgt.lower()
    ]    
    structures = []
    for node in bias_nodes:
        parents = [(src, rel) for (src, rel, tgt) in triples if tgt == node]
        children = [(rel, tgt) for (src, rel, tgt) in triples if src == node and rel != ':instance']
        siblings = set()
        for (src, rel, tgt) in triples:
            if tgt == node:
                siblings.update([sib_tgt for (sib_src, sib_rel, sib_tgt) in triples if sib_src == src and sib_tgt != node])
        
        # Root detection
        all_targets = {t for (_, _, t) in triples}
        is_root = node not in all_targets
        
        structures.append({
            "node": node,
            "is_root": is_root,
            "parents": parents,
            "siblings": list(siblings),
            "children": children
        })
    return structures


for i, graph in enumerate(amr_graphs):
    structures = analyze_bias_structure(graph)
    if structures:
        print(f"\n--- Graph {i+1} ---")
        for s in structures:
            print(f"Node: {s['node']} (root={s['is_root']})")
            print(f"  Parents: {s['parents']}")
            print(f"  Siblings: {s['siblings']}")
            print(f"  Children: {s['children']}")

summary = {
    "root_count": 0,
    "non_root_count": 0,
    "relations_to_bias": Counter(),
    "relations_from_bias": Counter(),
    "graphs_with_polarity": [],
}

for i, graph in enumerate(amr_graphs):
    triples = graph.triples
    bias_nodes = [src for (src, rel, tgt) in triples if rel == ":instance" and tgt and "bias" in tgt.lower()]
    for node in bias_nodes:
        # Root or not
        all_targets = {t for (_, _, t) in triples}
        if node not in all_targets:
            summary["root_count"] += 1
        else:
            summary["non_root_count"] += 1

        # Incoming and outgoing relations
        for src, rel, tgt in triples:
            if tgt == node:
                summary["relations_to_bias"][rel] += 1
            if src == node:
                summary["relations_from_bias"][rel] += 1
                if rel == ":polarity":
                    summary["graphs_with_polarity"].append(i+1)

# --- Print results ---
print("\n=== Summary of 'bias' structures ===")
print(f"Root occurrences: {summary['root_count']}")
print(f"Non-root occurrences: {summary['non_root_count']}")
print("\nRelations to 'bias' (parents):")
for rel, count in summary["relations_to_bias"].most_common():
    print(f"  {rel}: {count}")
print("\nRelations from 'bias' (children):")
for rel, count in summary["relations_from_bias"].most_common():
    print(f"  {rel}: {count}")
print(f"\nGraphs with polarity markers: {summary['graphs_with_polarity']}")


plt.figure(figsize=(6,4))
plt.bar(summary["relations_to_bias"].keys(), summary["relations_to_bias"].values())
plt.title("Relations to 'bias' (Parent Links)")
plt.xticks(rotation=45)
plt.ylabel("Frequency")

plot_path = 'figures/bias_amr.png'
plt.savefig(plot_path, dpi=300, bbox_inches="tight")
