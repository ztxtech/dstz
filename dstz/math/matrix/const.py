import numpy as np

BFRM = np.array([
    [1, 0],
    [1, 1]])

QFRM = np.array([
    [1, 1],
    [0, 1]])


def matrix_self_kron(matrix, n):
    res = 1
    for i in range(n):
        res = np.kron(res, matrix)
    return res


def get_qfrm(n):
    return matrix_self_kron(QFRM, n)


def get_bfrm(n):
    return matrix_self_kron(BFRM, n)
