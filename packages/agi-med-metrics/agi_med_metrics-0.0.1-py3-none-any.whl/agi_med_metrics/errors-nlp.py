from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

import evaluate

bleu_score = evaluate.load('bleu')
rouge_score = evaluate.load('rouge')
encoder = SentenceTransformer('multi-qa-distilbert-cos-v1')


def cosine_similarity_score(predictions, references):
    embs_true = encoder.encode(references)
    embs_pred = encoder.encode(predictions)
    return cos_sim(embs_true, embs_pred).diagonal().mean().item()  # NLP
