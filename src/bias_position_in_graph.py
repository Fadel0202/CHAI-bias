from penman import load
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import logging
from src.config import cfg

# --- Logging configuration ---
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("penman").setLevel(logging.ERROR)
logging.getLogger("penman.codec").setLevel(logging.ERROR)

# --- Load AMR file ---
amr_file = cfg.amr_path

with open(amr_file, "r", encoding="utf-8") as f:
    amr_graphs = list(load(f))

print(f"Loaded {len(amr_graphs)} AMR graphs.\n")

# --- Count occurrences of concepts related to 'bias' ---
bias_concepts = defaultdict(int)

for graph in amr_graphs:
    for src, rel, tgt in graph.triples:
        if rel == ":instance" and tgt and "bias" in tgt.lower():
            bias_concepts[tgt.lower()] += 1

# --- Analyze structural position of 'bias' in each graph ---
def analyze_bias_structure(graph):
    """Return structural info for nodes representing 'bias' or 'bias-01'."""
    triples = graph.triples
    bias_nodes = [
        src
        for (src, rel, tgt) in triples
        if rel == ":instance" and tgt and "bias" in tgt.lower()
    ]
    structures = []

    for node in bias_nodes:
        parents = [(src, rel) for (src, rel, tgt) in triples if tgt == node]
        children = [(rel, tgt) for (src, rel, tgt) in triples if src == node and rel != ":instance"]
        siblings = set()

        for (src, rel, tgt) in triples:
            if tgt == node:
                siblings.update(
                    [sib_tgt for (sib_src, sib_rel, sib_tgt) in triples if sib_src == src and sib_tgt != node]
                )

        all_targets = {t for (_, _, t) in triples}
        is_root = node not in all_targets
        is_leaf = not any(src == node and rel != ":instance" for (src, rel, tgt) in triples)

        structures.append({
            "node": node,
            "is_root": is_root,
            "is_leaf": is_leaf,
            "parents": parents,
            "siblings": list(siblings),
            "children": children
        })
    return structures


# --- Iterate and print structure info for graphs containing 'bias' ---
for i, graph in enumerate(amr_graphs):
    structures = analyze_bias_structure(graph)
    if structures:
        print(f"\n--- Graph {i + 1} ---")
        for s in structures:
            pos_type = "root" if s["is_root"] else "leaf" if s["is_leaf"] else "node"
            print(f"Node: {s['node']} ({pos_type})")
            print(f"  Parents: {s['parents']}")
            print(f"  Siblings: {s['siblings']}")
            print(f"  Children: {s['children']}")

summary = {
    "root_count": 0,
    "node_count": 0,
    "leaf_count": 0,
    "relations_to_bias": Counter(),
    "relations_from_bias": Counter(),
}

for graph in amr_graphs:
    triples = graph.triples
    bias_nodes = [src for (src, rel, tgt) in triples if rel == ":instance" and tgt and "bias" in tgt.lower()]

    for node in bias_nodes:
        all_targets = {t for (_, _, t) in triples}
        is_root = node not in all_targets
        is_leaf = not any(src == node and rel != ":instance" for (src, rel, tgt) in triples)

        if is_root:
            summary["root_count"] += 1
        elif is_leaf:
            summary["leaf_count"] += 1
        else:
            summary["node_count"] += 1

        for src, rel, tgt in triples:
            if tgt == node:
                summary["relations_to_bias"][rel] += 1
            if src == node:
                summary["relations_from_bias"][rel] += 1

print("\nRelations TO 'bias' (Parent → Bias):")
for rel, count in summary["relations_to_bias"].most_common():
    print(f"  {rel}: {count}")

print("\nRelations FROM 'bias' (Bias → Child):")
for rel, count in summary["relations_from_bias"].most_common():
    print(f"  {rel}: {count}")

# --- parent relations ---
plt.figure(figsize=(6, 4))
relations_to_bias = summary["relations_to_bias"]
if relations_to_bias:
    sorted_relations = sorted(relations_to_bias.items(), key=lambda x: x[1], reverse=True)
    relations, counts = zip(*sorted_relations)
    plt.bar(relations, counts, color="lightcoral")
    plt.title("Relations TO 'bias' (Parent Links)")
    plt.xticks(rotation=45)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("figures/relations_to_bias.png", dpi=300, bbox_inches="tight")

# --- child relations ---
plt.figure(figsize=(6, 4))
relations_from_bias = summary["relations_from_bias"]
if relations_from_bias:
    sorted_relations = sorted(relations_from_bias.items(), key=lambda x: x[1], reverse=True)
    relations, counts = zip(*sorted_relations)
    plt.bar(relations, counts, color="mediumseagreen")
    plt.title("Relations FROM 'bias' (Child Links)")
    plt.xticks(rotation=45)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("figures/relations_from_bias.png", dpi=300, bbox_inches="tight")
