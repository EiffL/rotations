"""
A function to rotate collectios of n-dimensional vectors
"""

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)
import numpy as np
from .vector_utilities import (elementwise_dot, elementwise_norm,
                               normalized_vectors, angles_between_list_of_vectors)


__all__=['rotate_vector_collection',]
__author__ = ['Duncan Campbell', 'Andrew Hearin']

def rotate_vector_collection(rotation_matrices, vectors, optimize=False):
    r"""
    Given a collection of rotation matrices and a collection of n-dimensional vectors,
    apply an asscoiated matrix to rotate corresponding vector(s).

    Parameters
    ----------
    rotation_matrices : ndarray
        The options are:
        1.) array of shape (npts, ndim, ndim) storing a collection of rotation matrices.
        2.) array of shape (ndim, ndim) storing a single rotation matrix
        3.) array of shape (nsets, ndim, ndim) storing a collection of rotation matrices.

    vectors : ndarray
        The corresponding options for above are:
        1.) array of shape (npts, ndim) storing a collection of ndim-dimensional vectors
        2.) array of shape (npts, ndim) storing a collection of ndim-dimensional vectors
        3.) array of shape (nsets, npts, ndim) storing a collection of ndim-dimensional vectors

    Returns
    -------
    rotated_vectors : ndarray
        Numpy array of shape (npts, ndim) storing a collection of ndim-dimensional vectors

    Notes
    -----
    This function is set up to preform either:
    1. rotation operations on a single collection of vectors,
    either applying a single rotation matrix to all vectors in the collection,
    or applying a unique rotation matrix to each vector in the set.
    2. applying a one rotation matrix to each collection of vectors.

    The behavior of the function is determined by the arguments supplied by the user.

    Examples
    --------
    In this example, we'll randomly generate two sets of unit-vectors, `v0` and `v1`.
    We'll use the `rotation_matrices_from_vectors` function to generate the
    rotation matrices that rotate each `v0` into the corresponding `v1`.
    Then we'll use the `rotate_vector_collection` function to apply each
    rotation, and verify that we recover each of the `v1`.

    >>> npts, ndim = int(1e4), 3
    >>> v0 = normalized_vectors(np.random.random((npts, ndim)))
    >>> v1 = normalized_vectors(np.random.random((npts, ndim)))
    >>> rotation_matrices = rotation_matrices_from_vectors(v0, v1)
    >>> v2 = rotate_vector_collection(rotation_matrices, v0)
    >>> assert np.allclose(v1, v2)
    """

    ndim_rotm = np.shape(rotation_matrices)[-1]
    ndim_vec = np.shape(vectors)[-1]

    assert ndim_rotm==ndim_vec

    # apply same rotation matrix to all vectors
    if (len(np.shape(rotation_matrices)) == 2):
        return np.dot(rotation_matrices, vectors.T).T

    # apply same rotation matrix to all vectors
    if (np.shape(rotation_matrices)[0] == 1):
        return np.dot(rotation_matrices[0], vectors.T).T

    # rotate each vector by associated rotation matrix
    else:
        # n1 sets of n2 vectors of ndim dimension
        if len(np.shape(vectors))==3:
            ein_string = 'ikl,ijl->ijk'
            n1, n2, ndim = np.shape(vectors)
        # n1 vectors of ndim dimension
        elif len(np.shape(vectors))==2:
            ein_string = 'ijk,ik->ij'
            n1, ndim = np.shape(vectors)

        try:
            return np.einsum(ein_string, rotation_matrices, vectors, optimize=optimize)
        except TypeError:
            return np.einsum(ein_string, rotation_matrices, vectors)


