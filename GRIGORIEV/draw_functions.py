from matplotlib import image as mpl
import numpy as np
import sympy


def draw_img(fn, arr):
    mpl.imsave(fn, arr, vmin=0, vmax=255, cmap="gray", origin="upper")


def draw_by_xy(xy, h, w, fn):
    matrix = matrix_by_xy(xy, h, w)
    matrix = (matrix - 1) * -255
    draw_img(fn, matrix)


def matrix_by_xy(xy, h, w):
    arr = np.zeros((h, w), dtype=np.int32)
    for i in xy:
        arr[i[0], i[1]] = 1
    return arr


def xy_from_matrix(matrix, h, w):
    xy = []
    for i in range(h):
        for j in range(w):
            if matrix[i, j] == 1:
                xy.append((i, j))
    return xy

def draw_line(lines, w, h):
    draw = np.zeros((w, h))
    pl = []
    x, y = sympy.symbols('x y')
    sympy.plot_implicit(sympy.Or(*[sympy.Eq(i[0] * x + i[1] * y + i[2]) for i in lines]), ('x', -100, 100), ('y', -100, 100))
