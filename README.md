# DeepPavlov at SemEval-2024 Task 8: Leveraging Transfer Learning for Detecting Boundaries of Machine-Generated Texts

This is a repository for SemEval204-Task8-subtaskC solution from DeepPavlov team. 
Our solution receives the best MAE score in accordance with the leaderboard (13.38).

![Pipeline for Data Augmentation](./pics/scheme_final_version.png)

Code for augmentation can be found [here](./src/data_augmentation.py).





<div align="center">
<h1>DeepPavlov at SemEval-2024 Task 8: Leveraging Transfer Learning for Detecting Boundaries of Machine-Generated Texts</h1>

[Anastasia Voznyuk](https://github.com/natriistorm)<sup>1 :email: *</sup>, Vasily Konovalov<sup>1</sup>

<sup>1</sup> Moscow Institute of Physics and Technology

<sup>:email:</sup> Corresponding author

[📝 Paper](https://github.com/kisnikser/Forecasting-fMRI-Images/blob/main/paper/main.pdf), [</> Code](https://github.com/kisnikser/Forecasting-fMRI-Images/tree/main/code)
</div>

## 💡 Abstract
The issue of reconstructing the relationship between functional magnetic resonance imaging (fMRI) sensor readings and human perception of the external is investigated. The study analyzes the dependence between the fMRI images and the videos viewed by individuals. Based on this analysis, a method is proposed for approximating the fMRI readings using the video sequence. The method is based on the assumption that there is a time-invariant hemodynamic response to changes in blood oxygen levels. A linear model is constructed for each individual voxel in the fMRI image, assuming that the image sequence follows a Markov property. To test the proposed method, a computational experiment was conducted on a dataset collected during tomographic examinations of a large number of individuals. The performance of the method was evaluated based on the experimental data, and hypotheses were tested regarding the invariance of the model weights and the correctness of the method.

## 🔎 Overview
<div align="center">
  <img alt="overview" src="https://github.com/natriistorm/SemEval2024-boundary-detection/blob/main/pics/scheme_final_version.png">
</div>

## 🛠️ Repository Structure
The repository is structured as follows:
- `paper`: This directory contains the main paper in PDF format (`main.pdf`) and the LaTeX source file (`main.tex`). Also there is a directory `figures` with images used in the paper.
- `code`: This directory contains the code used in the paper. It has its own `README.md` file providing a detailed description of the code files.
```shell
Forecasting-fMRI-Images
├── LICENSE
├── README.md
├── code
│   ├── README.md
│   ├── dataloader.py
│   ├── main.ipynb
│   ├── models.py
│   ├── utils.py
│   └── visualizer.py
└── paper
    ├── figs
    ├── main.pdf
    ├── main.tex
    ├── references.bib
    ├── sn-jnl.cls
    └── sn-mathphys-num.bst
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
