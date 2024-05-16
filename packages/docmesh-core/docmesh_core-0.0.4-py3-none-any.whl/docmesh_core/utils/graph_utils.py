import numpy as np
import numpy.typing as npt

from scipy.sparse import sparray


def find_max_degree_nodes(adj_mat: sparray) -> npt.NDArray[np.int_]:
    degs = adj_mat.sum(axis=0)
    degs_max_indices = np.flatnonzero(degs == degs.max())

    return degs_max_indices
