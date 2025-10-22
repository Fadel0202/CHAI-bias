# IA 717: CHAI & bias: linguistics of AI ethics charters & manifestos

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
   Extract all sentences containing bias-related words and save them to a CSV file:\
   File: `create_csv_sentence.py`
   → Output: `bias-MapAIE.csv`

2. **Bias Exploration**
   Visualize bias distribution and patterns across the dataset:\
   File: `bais_exploration.py`
   → Output: `bias_analysis_subplot.png`

3. **Word Frequency Analysis**
   Explore frequency of bias-related words:\
   File: `data_exploration.py`
   → Output: `word_frequency.png`

4. **POS Tag Visualization**
   Analyze part-of-speech patterns associated with biased words:\
   File: `bias_pos_tag.py`
   → Output: `bias_pos_visualisation.png`

---

### **Part 2: AMR Analysis**

5. **AMR Structure Exploration**
   Investigate structural bias representation within AMR graphs:\
   File: `bias_amr.py`
   → Output: summary of bias structure + `hist_concept.png` + `bias_amr.png`

6. **Bias Position in Graphs**
   Identify relationships from/to bias-related nodes in the AMR graph.\
   → Output: count relation TO / FROM bias + `relations_to_bias.png` + `relations_from_bias.png` 

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
│   └── bias-MapAIE.csv       # created with create_csv_sentence.py
│
├── mapaie/                   # clone from gitlab tiphaine.viard/mapaie
|   ├── ...
│   ├── docs/
│   └── txts/
│
├── src/
│   ├── bias_exploration.py
│   ├── bias_pos_tag.py
│   ├── bias_amr.py
│   └── ...
│
├── config.json
└── README.md
```
