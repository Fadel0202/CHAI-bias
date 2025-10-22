import os
import re
from nltk.corpus import stopwords
import nltk
import pandas as pd
from src.config import cfg

# --- Setup ---
nltk.download("stopwords", quiet=True)
stop_words = set(stopwords.words("english"))

text_dir = cfg.txt_path
csv_file = cfg.MapAIE_csv_path

bias_sentences = []

# Loop over each document
for filename in os.listdir(text_dir):
    if filename.endswith(".txt"):
        doc_id = re.sub(r"\D", "", filename)  # extract number from filename
        with open(os.path.join(text_dir, filename), "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            # Split into sentences
            sentences = nltk.sent_tokenize(text)
            # Keep only those containing "bias"
            for s in sentences:
                if "bias" in s.lower():
                    bias_sentences.append({"doc_id": doc_id, "sentence": s.strip()})

# Convert to DataFrame for organization
bias_df = pd.DataFrame(bias_sentences)

# Display size of bias-MapAIE corpus
print(f"The bias-MapAIE corpus contains {len(bias_df)} sentences.")

# Optional: show first few rows
print(bias_df.head())

# Save corpus to CSV if needed
bias_df.to_csv(
    csv_file, 
    index=False,
    quoting=1,
    escapechar="\\", # escape special characters
    encoding="utf-8"
)