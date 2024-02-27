# semeval2024-machine-generated-texts-detection

This is a repository for SemEval204-Task8-subtaskC from DeepPavlov team. Our solution recieves best MAE score in accoradance with the leaderboard.

Pipeline for Data Augmentation:

![Pipeline for Data Augmentation](./pics/scheme3.png)

Code can be found [here](./src/data_augmentation.py)

Files [here](./best_prediction) gives the best MAE score on test dataset (15.20903). It didn't appear on the leaderboard, because our final submission was trained with the wrong tokenizer (it was a bug) and we obtained 18.2435 score, but the same pipeline with matching tokenizer allowed us to improve our score and outperform the top-1 solution from the leaderboard.
