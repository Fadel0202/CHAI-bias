import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
from src.config import cfg

# Download NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')

csv_path=cfg.MapAIE_csv_path
bias_df = pd.read_csv(csv_path)

# Function to extract the POS tag for the word 'bias'
def get_bias_pos(sentence):
    words = word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)
    for word, tag in pos_tags:
        if word.lower() == 'bias':
            return tag
    return None

# Apply the function to each sentence
bias_df['bias_pos'] = bias_df['sentence'].apply(get_bias_pos)

# Count the frequency of each POS tag for 'bias'
pos_counts = bias_df['bias_pos'].value_counts()

# Plotting
plt.figure(figsize=(10, 6))
pos_counts.plot(kind='bar', edgecolor='black')
plt.title('Syntactic Roles of the Term "bias" in the Corpus')
plt.xlabel('POS Tag')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

plot_path = 'data/bias_pos_visualization.png'
plt.savefig(plot_path, dpi=300, bbox_inches="tight")

plt.show()
