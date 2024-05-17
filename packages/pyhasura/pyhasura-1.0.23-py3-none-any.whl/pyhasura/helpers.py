def get_ordinal_of_smallest_number(numbers):
    m = None
    n = None
    for i, x in enumerate(numbers):
        if m is None:
            m = x
            n = i
        if x != 0 and x < m:
            m = x
            n = i
    return n


def compute_deltas(numbers):
    """
    Computes the deltas (differences) between consecutive elements in an array of numbers.

    Args:
        numbers (list or numpy.ndarray): Input array of numbers.

    Returns:
        list: Array of deltas (differences) between consecutive elements.
    """
    deltas = []
    if len(numbers) <= 1:
        deltas.append(0)
    else:
        for i in range(1, len(numbers)):
            delta = numbers[i] - numbers[i - 1]
            deltas.append(abs(delta))
    return deltas
