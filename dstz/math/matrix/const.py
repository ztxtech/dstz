import numpy as np

# Belief Function Relation Matrix (BFRM) for a single element.
# Used for transformations between mass functions and belief/plausibility functions.
BFRM = np.array([
    [1, 0],
    [1, 1]])

# Commonality Function Relation Matrix (QFRM) for a single element.
# Used for transformations between mass functions and commonality functions.
QFRM = np.array([
    [1, 1],
    [0, 1]])


def matrix_self_kron(matrix, n):
    """Computes the n-th Kronecker power of a matrix.

    This function repeatedly calculates the Kronecker product of a matrix with
    itself `n` times.

    Args:
        matrix (np.ndarray): The input matrix.
        n (int): The number of times to perform the Kronecker product.

    Returns:
        np.ndarray: The resulting matrix from the repeated Kronecker product.
    """
    res = 1
    for i in range(n):
        res = np.kron(res, matrix)
    return res


def get_qfrm(n):
    """Generates the Commonality Function Relation Matrix for a space of size n.

    Args:
        n (int): The size of the Frame of Discernment.

    Returns:
        np.ndarray: The QFRM matrix of size 2^n x 2^n.
    """
    return matrix_self_kron(QFRM, n)


def get_bfrm(n):
    """Generates the Belief Function Relation Matrix for a space of size n.

    Args:
        n (int): The size of the Frame of Discernment.

    Returns:
        np.ndarray: The BFRM matrix of size 2^n x 2^n.
    """
    return matrix_self_kron(BFRM, n)