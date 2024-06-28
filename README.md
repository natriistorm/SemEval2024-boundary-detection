# DeepPavlov at SemEval-2024 Task 8: Leveraging Transfer Learning for Detecting Boundaries of Machine-Generated Texts

This is a repository for SemEval204-Task8-subtaskC solution from DeepPavlov team. The [repository](https://github.com/mbzuai-nlp/SemEval2024-task8) with all information about competition.

Our solution receives the best MAE score in accordance with the leaderboard (13.38). while the best result in leaderboard in 15.68).

Pipeline for Data Augmentation:

![Pipeline for Data Augmentation](./pics/scheme_final_version.png)

Code for augmentation can be found [here](./src/data_augmentation.py).

@inproceedings{voznyuk-konovalov-2024-deeppavlov,
    title = "{D}eep{P}avlov at {S}em{E}val-2024 Task 8: Leveraging Transfer Learning for Detecting Boundaries of Machine-Generated Texts",
    author = "Voznyuk, Anastasia  and
      Konovalov, Vasily",
    editor = {Ojha, Atul Kr.  and
      Do{\u{g}}ru{\"o}z, A. Seza  and
      Tayyar Madabushi, Harish  and
      Da San Martino, Giovanni  and
      Rosenthal, Sara  and
      Ros{\'a}, Aiala},
    booktitle = "Proceedings of the 18th International Workshop on Semantic Evaluation (SemEval-2024)",
    month = jun,
    year = "2024",
    address = "Mexico City, Mexico",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.semeval-1.257",
    pages = "1821--1829",
    abstract = "The Multigenerator, Multidomain, and Multilingual Black-Box Machine-Generated Text Detection shared task in the SemEval-2024 competition aims to tackle the problem of misusing collaborative human-AI writing. Although there are a lot of existing detectors of AI content, they are often designed to give a binary answer and thus may not be suitable for more nuanced problem of finding the boundaries between human-written and machine-generated texts, while hybrid human-AI writing becomes more and more popular. In this paper, we address the boundary detection problem. Particularly, we present a pipeline for augmenting data for supervised fine-tuning of DeBERTaV3. We receive new best MAE score, according to the leaderboard of the competition, with this pipeline.",
}
