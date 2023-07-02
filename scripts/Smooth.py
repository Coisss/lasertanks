def exponential_decay_smoothing(previous_value, end, alpha):
    return alpha * end + (1 - alpha) * previous_value