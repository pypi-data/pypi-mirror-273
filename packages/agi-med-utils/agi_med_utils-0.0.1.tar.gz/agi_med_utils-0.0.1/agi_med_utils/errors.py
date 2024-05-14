from sklearn.metrics import confusion_matrix
import evaluate
from nltk import edit_distance
import numpy as np
from tqdm.contrib.concurrent import process_map
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


bleu_score = evaluate.load('bleu')
rouge_score = evaluate.load('rouge')
encoder = SentenceTransformer('multi-qa-distilbert-cos-v1')


def values(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return tn, fp, fn, tp


def false_positive_rate_score(y_true, y_pred):
    tn, fp, fn, tp = values(y_true, y_pred)
    return fp / (fp + tn)


def false_negative_rate_score(y_true, y_pred):
    tn, fp, fn, tp = values(y_true, y_pred)
    return fn / (fn + tp)


def edit_dist_pairs(pair):
    return edit_distance(*pair)


def mean_char_error_rate_score(text_trues, text_preds) -> float:
    text_lens = process_map(len, text_trues, disable=True)
    edit_dists = process_map(edit_dist_pairs, list(zip(*[text_trues, text_preds])))
    return np.sum(edit_dists) / np.sum(text_lens)


def cosine_similarity_score(predictions, references):
    embs_true = encoder.encode(references)
    embs_pred = encoder.encode(predictions)
    return cos_sim(embs_true, embs_pred).diagonal().mean().item()
