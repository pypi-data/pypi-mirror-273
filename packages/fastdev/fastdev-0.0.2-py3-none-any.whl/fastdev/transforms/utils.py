import numpy as np


def compose_intr_mat(fu: float, fv: float, cu: float, cv: float, skew: float = 0.0):
    """
    Args:
        fu: horizontal focal length (width)
        fv: vertical focal length (height)
        cu: horizontal principal point (width)
        cv: vertical principal point (height)
        skew: skew coefficient, default to 0
    """
    intr_mat = np.array([[fu, skew, cu], [0.0, fv, cv], [0.0, 0.0, 1.0]], dtype=np.float32)
    return intr_mat
