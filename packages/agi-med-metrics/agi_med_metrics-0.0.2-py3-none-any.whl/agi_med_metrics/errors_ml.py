from sklearn.metrics import confusion_matrix


def values(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return tn, fp, fn, tp


def false_positive_rate_score(y_true, y_pred):
    tn, fp, fn, tp = values(y_true, y_pred)
    return fp / (fp + tn)


def false_negative_rate_score(y_true, y_pred):
    tn, fp, fn, tp = values(y_true, y_pred)  # ML
    return fn / (fn + tp)
