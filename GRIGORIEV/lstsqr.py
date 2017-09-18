from numpy.linalg import lstsq
import numpy as np


def fivePointsToConic(points, f=1.0):
        x = points[:, 0]
        y = points[:, 1]
        if max(x.shape) < 5:
            raise ValueError('Need >= 5 points to solve for conic section')

        A = np.vstack([x**2, x * y, y**2, x, y]).T
        fullSolution = lstsq(A, f * np.ones(x.size))
        (a, b, c, d, e) = fullSolution[0]

        return (a, b, c, d, e, f)