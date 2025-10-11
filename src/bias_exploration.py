import os
import math
import string
import unicodedata
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk
from src.config import cfg

# --- Setup ---
nltk.download("stopwords", quiet=True)
stop_words = set(stopwords.words("english"))

text_dir = cfg.txt_path
if not os.path.exists(text_dir):
    raise FileNotFoundError(f"Text folder not found: {text_dir}")

# --- 1️ Count 'bias' occurrences ---
bias_counts = {}
for filename in os.listdir(text_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(text_dir, filename)
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().lower()
            bias_counts[filename] = text.count("bias")

sorted_docs = sorted(bias_counts.items(), key=lambda x: x[1], reverse=True)
if not sorted_docs:
    exit()

top_n = max(1, math.ceil(len(sorted_docs) * 0.1))
top_docs = sorted_docs[:top_n]
print(f"\nTop {top_n} ({round(top_n / len(sorted_docs) * 100, 1)}%) documents with most 'bias' occurrences:")
for doc, count in top_docs:
    print(f"  {doc}: {count}")

# --- 2️ Extract collocations around 'bias' ---
window_size = 5
contexts = []

for doc, _ in top_docs:
    file_path = os.path.join(text_dir, doc)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        words = [w.strip(string.punctuation) for w in f.read().lower().split()]
        for i, word in enumerate(words):
            if word == "bias":
                left_context = " ".join(words[max(0, i - window_size):i])
                right_context = " ".join(words[i + 1:i + 1 + window_size])
                contexts.append((left_context, "bias", right_context))

ngrams = []
for left, center, right in contexts:
    left_parts = left.split()
    right_parts = right.split()
    if left_parts:
        ngrams.append(f"{left_parts[-1]} bias")
    if right_parts:
        ngrams.append(f"bias {right_parts[0]}")

ngram_freq = Counter(ngrams)
top_ngrams = ngram_freq.most_common(27)

# --- 3️ Broader context words around 'bias' ---
window_size = 5
context_words = []
for doc, _ in top_docs:
    file_path = os.path.join(text_dir, doc)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = unicodedata.normalize("NFKC", f.read().lower())
        words = [w.strip(string.punctuation + "•") for w in text.split()]
        for i, word in enumerate(words):
            if word == "bias":
                left_context = words[max(0, i - window_size):i]
                right_context = words[i + 1:i + 1 + window_size]
                context_words.extend(left_context + right_context)

# Clean and count
context_filtered = []
for w in context_words:
    w = "".join(ch for ch in w if not unicodedata.category(ch).startswith("C"))
    if w and w not in stop_words and w != "bias":
        context_filtered.append(w)

context_freq = Counter(context_filtered)
top_context = context_freq.most_common(15)

fig, axes = plt.subplots(3, 1, figsize=(12, 14))
fig.suptitle("‘Bias’ Analysis Across Corpus", fontsize=16, fontweight="bold")

# Plot 1: Top biased documents
docs, counts = zip(*top_docs)
axes[0].bar(docs, counts, color="skyblue")
axes[0].set_title(f"Top {top_n} Documents with Most 'Bias' Occurrences")
axes[0].set_ylabel("Count")
axes[0].tick_params(axis="x", rotation=45)

# Plot 2: Top collocations
if top_ngrams:
    ngram_labels, ngram_counts = zip(*top_ngrams)
    axes[1].bar(ngram_labels, ngram_counts, color="lightgreen")
    axes[1].set_title("Most Frequent Collocations with 'bias'")
    axes[1].set_ylabel("Frequency")
    axes[1].tick_params(axis="x", rotation=45)

# Plot 3: Context words
if top_context:
    words, freqs = zip(*top_context)
    axes[2].bar(words, freqs, color="salmon")
    axes[2].set_title(f"Top Context Words Around 'bias' (±{window_size} words)")
    axes[2].set_ylabel("Frequency")
    axes[2].tick_params(axis="x", rotation=45)

plt.tight_layout(rect=[0, 0, 1, 0.96])

# --- Save subplot figure ---
output_dir = os.path.join("data")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "bias_analysis_subplots.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close()

# --- Print summaries ---
print("\nTop collocations with 'bias':")
for ng, freq in top_ngrams:
    print(f"  {ng}: {freq}")

print("\nTop context words around 'bias':")
for word, freq in top_context:
    print(f"  {word}: {freq}")
