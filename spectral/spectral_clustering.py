#CODE FOR UNNORMALIZED SPECTRAL CLUSTERING
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
from scipy.linalg import eigh

def get_init_vectors(filename):
    """
    * Returns the vectors after reading from file
    * Converts to numpy array
    """

    fp = open(filename)
    lines = fp.readlines()
    fp.close()

    arr = []
    for each in lines:
        arr.append(each.strip().split(','))

    return np.asarray(arr)

def get_weighted_matrix(matrix, k):
    """
    * Uses the k nearest neighbor similarity criterion
    """

    weight_arr = np.zeros((len(matrix), len(matrix)))
    
    # computes pairwise distances
    dist_arr = euclidean_distances(matrix)

    # computes the k nearest
    for i in xrange(0, len(dist_arr)):
        karr = np.argpartition(dist_arr[i], -k)[-k:]
        for every in karr:
            weight_arr[i][every] = dist_arr[i][every]

    return weight_arr

def get_degree_matrix(w_matrix):
    """
    * Returns the degree matrix
    """

    degree_matrix = np.identity(len(w_matrix))
    for i in xrange(0, len(w_matrix)):
        val = 0
        for each in w_matrix[i]:
            val += each
        degree_matrix[i][i] = val

    return degree_matrix

def get_laplacian(D, W):
    """
     * Returns the Laplcian Matrix
    """

    return D - W

def compute_vectors(L, k):
    """
    * Computes the new vectors to be clustered
    """
    arr = []
    eigenvals, eigenvecs = eigh(L)
    count = 0
    for i in xrange(0, len(eigenvals)):
        if count == k:
            break
        if eigenvals[i] > 0:
            print eigenvecs[i]
            arr.append(eigenvecs[i])
            count += 1

    return arr

def main():
    arr = get_init_vectors('../data/data1.csv')
    weighted_arr = get_weighted_matrix(arr, 5)
    deg_matrix = get_degree_matrix(weighted_arr)
    laplace = get_laplacian(deg_matrix, weighted_arr)
    new_vectors = compute_vectors(laplace, 5)
main()
