# 🧠 CHAI Bias

A toolkit for exploring and visualizing linguistic bias in text and AMR (Abstract Meaning Representation) data.

---

## ⚙️ Setup

### 1. Configure paths

Edit your `config.json` file to specify the correct paths for your data:

```json
{
  "txt_path": ".../mapaie/data/txts",
  "MapAIE_csv_path": "bias-MapAIE.csv",
  "amr_path": "data/bias_AMR-500_clean.amr"
}
```

### 2. Run the pipeline

Execute your desired module from the `src` directory:

```bash
python -m src.<module_name>
```

---

## Pipeline Overview
### **Part 0 : Download data**
Follow step by step this repository to finally obtain txts/ folder :

https://gitlab.telecom-paris.fr/tiphaine.viard/mapaie

### **Part 1: CSV and TXT Processing**

1. **Create CSV from text files**
   Extract all sentences containing bias-related words and save them to a CSV file:
   → Output: `bias-MapAIE.csv`

2. **Bias Exploration**
   Visualize bias distribution and patterns across the dataset:
   → Output: `bias_analysis_subplot.png`

3. **Word Frequency Analysis**
   Explore frequency of bias-related words:
   → Output: `word_frequency.png`

4. **POS Tag Visualization**
   Analyze part-of-speech patterns associated with biased words:
   → Output: `bias_pos_visualisation.png`

---

### **Part 2: AMR Analysis**

5. **AMR Structure Exploration**
   Investigate structural bias representation within AMR graphs:
   → Output: `bias_amr.png`

6. **Bias Position in Graphs**
   Identify relationships from/to bias-related nodes in the AMR graph.

---

## 📊 Graph Visualization

You can visualize AMR graphs interactively using **Metamorphosed** (Docker-based):

```bash
docker pull jheinecke/metamorphosed:latest

docker run --name metamorphosed -p 4567:4567 \
  --volume /home/ambroise012/CHAI-bias/data:/data \
  --env AMRFILE=bias-small.amr \
  jheinecke/metamorphosed:latest
```

Then, open your browser and navigate to:

👉 [http://localhost:4567/](http://localhost:4567/)

---

## 📁 Project Structure

```
CHAI-bias/
│
├── data/
│   ├── bias-AMR-500_clean.amr
│   └── bias-MapAIE.csv
│
├── mapaie/
│   ├── docs/
│   └── txts/
│
├── src/
│   ├── bias_exploration.py
│   ├── bias_pos_tag.py
│   ├── bias_amr.py
│   └── ...
│
├── notebooks/
│   └── bias_analysis.ipynb
│
├── config.json
└── README.md
```

---

## 🧾 Outputs Summary

| Step | Description            | Output File                  |
| ---- | ---------------------- | ---------------------------- |
| 1    | Extract bias sentences | `bias-MapAIE.csv`            |
| 2    | Bias analysis plots    | `bias_analysis_subplot.png`  |
| 3    | Word frequency plot    | `word_frequency.png`         |
| 4    | POS visualization      | `bias_pos_visualisation.png` |
| 5    | AMR structural bias    | `bias_amr.png`               |

---

Would you like me to make it **more formal and research-paper style** (for publication/code release), or **more practical and developer-oriented** (for contributors)? I can tailor the tone accordingly.
