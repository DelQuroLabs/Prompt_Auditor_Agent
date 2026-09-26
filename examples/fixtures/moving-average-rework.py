def moving_average(values, window):
    # The first rework fixed the final-window bound but forgot that bool is an int subclass.
    if not isinstance(window, int) or window <= 0:
        raise ValueError("window must be a positive integer")
    if window > len(values):
        return []
    return [
        sum(values[start:start + window]) / window
        for start in range(len(values) - window + 1)
    ]
