import os
import string
import re
from collections import Counter
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

from src.config import cfg

# --- Setup ---
nltk.download('stopwords', quiet=True)
nltk.download("punkt", quiet=True)

# --- Load all .txt files from cfg.txt_path ---
corpus_text = ""
if not os.path.exists(cfg.txt_path):
    raise FileNotFoundError(f"Text path not found: {cfg.txt_path}")

for filename in os.listdir(cfg.txt_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(cfg.txt_path, filename)
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            corpus_text += f.read().lower() + " "

print(f"Loaded {len(corpus_text)} characters from text files in '{cfg.txt_path}'.")

# --- Tokenization & Cleaning ---
# Extract alphabetic words only (length >= 2)
tokens = re.findall(r"\b[a-zA-Z]{2,}\b", corpus_text)

# Remove stopwords
stop_words = set(stopwords.words("english"))
filtered_tokens = [w for w in tokens if w not in stop_words]

# --- Frequency analysis ---
word_freq = Counter(filtered_tokens)
top_words = word_freq.most_common(40)

# Print top words
print("\nTop 40 most frequent words (excluding stopwords):")
for word, freq in top_words:
    print(f"{word}: {freq}")

# --- Visualization ---
plt.figure(figsize=(12, 6))
words, counts = zip(*top_words)
plt.bar(words, counts)
plt.title("Top 40 Most Frequent Words (Excluding Stopwords)")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Frequency")
plt.tight_layout()

# --- Save chart ---
output_dir = os.path.join("data")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "word_frequency.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"\nGraph saved to: {output_path}")
