<div align="center">
<h1>DeepPavlov at SemEval-2024 Task 8: Leveraging Transfer Learning for Detecting Boundaries of Machine-Generated Texts</h1>

[Anastasia Voznyuk](https://github.com/natriistorm)<sup>1 :email: *</sup>, Vasily Konovalov<sup>1</sup>

<sup>1</sup> Moscow Institute of Physics and Technology

<sup>:email:</sup> Corresponding author

[📝 Paper](https://aclanthology.org/2024.semeval-1.257/), [</> Code](https://github.com/natriistorm/SemEval2024-boundary-detection/tree/main/src)
</div>

## 💡 Abstract
The Multigenerator, Multidomain, and Multilingual Black-Box Machine-Generated Text Detection shared task in the SemEval-2024 competition aims to tackle the problem of misusing collaborative human-AI writing. Although there are a lot of existing detectors of AI content, they are often designed to give a binary answer and thus may not be suitable for more nuanced problem of finding the boundaries between human-written and machine-generated texts, while hybrid human-AI writing becomes more and more popular. In this paper, we address the boundary detection problem. Particularly, we present a pipeline for augmenting data for supervised fine-tuning of DeBERTaV3. We receive new best MAE score, according to the leaderboard of the competition, with this pipeline.

## 🔎 Overview
<div align="center">
  <img alt="overview" src="https://github.com/natriistorm/SemEval2024-boundary-detection/blob/main/pics/scheme_final_version.png">
</div>

## 🛠️ Repository Structure
The repository is structured as follows:
- `src`: This directory contains the code used in the paper and for submission.
```shell
Forecasting-fMRI-Images
├── LICENSE
├── README.md
├── code
│   ├── run.sh # shell script to load transformer_baseline and start experiment
│   ├── data_augmentation.py # main file for augmentation
│   ├── transformer_baseline.py # file to run experiments
│   ├── splitter.py # util file for splitting the texts
│   └── scorer.py # file to calculate MAE
└── 
```

## 🔎 Citation
```
@inproceedings{voznyuk-konovalov-2024-deeppavlov,
    title = "{D}eep{P}avlov at {S}em{E}val-2024 Task 8: Leveraging Transfer Learning for Detecting Boundaries of Machine-Generated Texts",
    author = "Voznyuk, Anastasia  and
      Konovalov, Vasily",
    booktitle = "Proceedings of the 18th International Workshop on Semantic Evaluation (SemEval-2024)",
    month = jun,
    year = "2024",
    address = "Mexico City, Mexico",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.semeval-1.257",
    pages = "1821--1829"
}
```
