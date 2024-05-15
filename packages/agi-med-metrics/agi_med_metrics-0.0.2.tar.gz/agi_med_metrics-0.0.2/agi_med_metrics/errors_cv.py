from nltk import edit_distance
import numpy as np
from tqdm.contrib.concurrent import process_map


def edit_dist_pairs(pair):
    return edit_distance(*pair)


def mean_char_error_rate_score(text_trues, text_preds) -> float:
    text_lens = process_map(len, text_trues, disable=True)
    edit_dists = process_map(edit_dist_pairs, list(zip(*[text_trues, text_preds])))
    return np.sum(edit_dists) / np.sum(text_lens)  # CV
