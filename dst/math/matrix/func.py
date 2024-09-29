def get_ones_indices(n):
    indices = []
    index = 0
    while n:
        if n & 1:
            indices.append(index)
        n >>= 1
        index += 1
    return indices
