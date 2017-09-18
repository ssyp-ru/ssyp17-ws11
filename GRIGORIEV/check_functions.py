from config import *


def check_table(binpix, i, j, num):
    slc = binpix[i - 1: i + 2, j - 1: j + 2]
    if num == 0:
        return slc[0, 0] == 1 and slc[0, 1] == 1 and slc[1, 0] == 1 and \
           slc[1, 2] == 0 and slc[2, 0] == 1 and slc[2, 1] == 1 and \
           (slc[2, 0] == 0 or slc[2, 2] == 0)
    elif num == 1:
        return slc[0, 1] == 1 and slc[0, 2] == 1 and slc[1, 2] == 0 and \
               slc[2, 1] == 0 and slc[1, 0] == 1 and slc[0, 0] == 1 and \
               (slc[0, 2] == 0 or slc[2, 2] == 0)
    elif num == 2:
        slc = binpix[i - 1: i + 2, j - 1: j + 3]
        return slc[0, 1] == 1 and slc[0, 2] == 1 and slc[1, 0] == 0 and \
               slc[1, 2] == 1 and slc[1, 3] == 1 and slc[2, 1] == 1 and \
               slc[2, 2] == 1 and (slc[0, 0] == 0 or slc[2, 0] == 0)
    elif num == 3:
        slc = binpix[i - 1: i + 3, j - 1: j + 2]
        return slc[0, 1] == 0 and slc[1, 0] == 1 and slc[1, 2] == 1 and \
               slc[2, 0] == 1 and slc[2, 1] == 1 and slc[2, 2] == 1 and \
               slc[3, 1] == 1 and (slc[0, 0] == 0 or slc[0, 2] == 0)
    elif num == 4:
        return slc[0, 1] == 0 and slc[0, 2] == 0 and slc[1, 0] == 1 and \
               slc[1, 2] == 0 and slc[2, 1] == 1
    elif num == 5:
        return slc[0, 1] == 1 and slc[0, 2] == 1 and slc[1, 0] == 0 and \
               slc[1, 2] == 1 and slc[2, 1] == 0 and slc[2, 0] == 0
    elif num == 6:
        return slc[0, 0] == 0 and slc[0, 1] == 1 and slc[0, 2] == 0 and \
               slc[1, 0] == 0 and slc[1, 2] == 1 and \
               slc[2, 0] == 0 and slc[2, 1] == 0 and slc[2, 2] == 0
    elif num == 7:
        return slc[0, 1] == 1 and \
               slc[1, 0] == 1 and slc[1, 2] == 0 and \
               slc[2, 1] == 0 and slc[2, 2] == 0
    elif num == 8:
        return slc[0, 0] == 0 and slc[0, 1] == 0 and \
               slc[1, 0] == 0 and slc[1, 2] == 1 and \
               slc[2, 1] == 1 and slc[2, 2] == 1
    elif num == 9:
        return slc[0, 0] == 0 and slc[0, 1] == 0 and slc[0, 2] == 0 and \
               slc[1, 0] == 0 and slc[1, 2] == 1 and \
               slc[2, 0] == 0 and slc[2, 1] == 1 and slc[2, 2] == 0
    elif num == 10:
        return slc[0, 0] == 0 and slc[0, 1] == 0 and slc[0, 2] == 0 and \
               slc[1, 0] == 0 and slc[1, 2] == 0 and \
               slc[2, 0] == 1 and slc[2, 1] == 1 and slc[2, 2] == 1
    elif num == 11:
        return slc[0, 0] == 1 and slc[0, 1] == 0 and slc[0, 2] == 0 and \
               slc[1, 0] == 1 and slc[1, 2] == 0 and \
               slc[2, 0] == 1 and slc[2, 1] == 0 and slc[2, 2] == 0
    elif num == 12:
        return slc[0, 0] == 1 and slc[0, 1] == 1 and slc[0, 2] == 1 and \
               slc[1, 0] == 0 and slc[1, 2] == 0 and \
               slc[2, 0] == 0 and slc[2, 1] == 0 and slc[2, 2] == 0
    elif num == 13:
        return slc[0, 0] == 0 and slc[0, 1] == 0 and slc[0, 2] == 1 and \
               slc[1, 0] == 0 and slc[1, 2] == 1 and \
               slc[2, 0] == 0 and slc[2, 1] == 0 and slc[2, 2] == 1


def is_alfa(nearest):
    for counter in range(4):
        if alfa_key(nearest, counter):
            return Правда
    return Кривда


def alfa_key(nearest, num):
    if num == 0:
        return is_all_equal(nearest, (1, 3), 1)
    elif num == 1:
        return is_all_equal(nearest, (3, 5), 1)
    elif num == 2:
        return is_all_equal(nearest, (5, 7), 1)
    elif num == 3:
        return is_all_equal(nearest, (1, 7), 1)


def is_beta(nearest, binpix, i, j):
    for counter in range(8):
        if beta_key(nearest, binpix, i, j, counter):
            return Правда
    return Кривда


def beta_key(nearest, binpix, i, j, num):
    if num == 0:
        return is_all_equal(nearest, (0, 3), 1) and binpix[i, j + 2] + binpix[i + 1, j + 2] >= 1
    elif num == 1:
        return is_all_equal(nearest, (0, 5), 1) and binpix[i, j - 2] + binpix[i + 1, j - 2] >= 1
    elif num == 2:
        return is_all_equal(nearest, (2, 5), 1) and binpix[i + 2, j] + binpix[i + 2, j - 1] >= 1
    elif num == 3:
        return is_all_equal(nearest, (1, 4), 1) and binpix[i, j + 2] + binpix[i - 1, j + 2] >= 1
    elif num == 4:
        return is_all_equal(nearest, (7, 2), 1) and binpix[i - 2, j] + binpix[i - 2, j - 1] >= 1
    elif num == 5:
        return is_all_equal(nearest, (7, 4), 1) and binpix[i, j - 2] + binpix[i - 1, j - 2] >= 1
    elif num == 6:
        return is_all_equal(nearest, (1, 6), 1) and binpix[i - 2, j] + binpix[i - 2, j + 1] >= 1
    elif num == 7:
        return is_all_equal(nearest, (3, 6), 1) and binpix[i + 2, j] + binpix[i + 2, j + 1] >= 1


def is_gamma(nearest, binpix, i, j):
    return (is_all_equal(nearest, (-1, 3), 1) and binpix[i + 2, j] + binpix[i, j + 2] >= 1 and
            binpix[i - 2, j] + binpix[i, j - 2] >= 1) or (
           is_all_equal(nearest, (1, -3), 1) and binpix[i - 2, j] + binpix[i, j + 2] >= 1 and
           binpix[i + 2, j] + binpix[i, j - 2] >= 1)


def is_all_equal(col, indices, value):
    if col.count(value) != len(indices):
        return Кривда
    for i in indices:
        if col[i] != value:
            return Кривда
    return Правда
