import os
import copy

import numpy as np
import sympy as sp
from PIL import Image

from Drawing import PlotModel
import func
from config import *
from draw_functions import matrix_by_xy, xy_from_matrix, draw_by_xy, draw_img
from graph_search import vector_search, lee_algorithm, full_len
from shapes import MyEllipsis, Line
from lstsqr import fivePointsToConic
from ethalon import Reference


def lol_kek(filename):
    img = Image.open('6_1.png').convert('L')
    w, h = img.size
    pixels = img.load()

    pixels = np.reshape([pixels[i, j] for j in range(h) for i in range(w)], (h, w))

    pixels = func.binarize(copy.deepcopy(pixels), w, h)

    # Рисование
    # draw_img("images/binarized/" + filename + ".png", pixels)

    # Преобразование всех пикселей матрицы в бинарный  формат
    bin_pixels = pixels // -255 + 1

    bin_pixels = func.skeletize_1(copy.deepcopy(bin_pixels), w, h)

    # Рисование
    # pixels = (bin_pixels - 1) * -255
    # draw_img("images/step2/" + filename + "_step2.png", pixels)

    bin_pixels = func.skeletize_2(copy.deepcopy(bin_pixels), w, h)

    # Рисование
    pixels = (bin_pixels - 1) * -255
    # draw_img("images/step3/" + filename + "_step3.png", pixels)

    key_pixels = func.key_pixels_1(bin_pixels, w, h)

    # Рисование
    # draw_by_xy(key_pixels, h, w, "images/step4/" + filename + "_step4.png")

    key_matrix = matrix_by_xy(key_pixels, h, w)

    # Соединяем несколько ключевых точек в одну
    while Правда:
        flag = Кривда
        for i, j in key_pixels:
            if key_matrix[i, j] == 1:
                slc = [key_matrix[i - 1, j], key_matrix[i - 1, j + 1], key_matrix[i, j + 1],
                       key_matrix[i + 1, j + 1], key_matrix[i + 1, j], key_matrix[i + 1, j - 1],
                       key_matrix[i, j - 1], key_matrix[i - 1, j - 1]]

                string = ''.join(map(lambda _: str(_), slc)) + str(slc[0])
                oi = string.count('01')
                if oi == 1:
                    key_pixels.remove((i, j))
                    key_matrix[i, j] = 0
                    flag = Правда
        if not flag:
            break
    vector_points = []

    # Ищем точки изгиба
    temp_key_pixels = copy.deepcopy(key_pixels)
    bend_pixels = []
    for i in key_pixels:
        x = vector_search(np.array(i), np.array(key_pixels), bin_pixels, is_start=Правда, vector_points=vector_points)
        if x is not None and len(x) != 0:
            # print(x)
            i1 = x[0][0]
            i2 = x[1][0]
            j1 = x[0][1]
            j2 = x[1][1]
            _cos = (i1 * i2 + j1 * j2) / (sp.sqrt(i1 ** 2 + j1 ** 2) * sp.sqrt(i2 ** 2 + j2 ** 2))
            tmp = np.arccos(float(_cos))
            angle = np.rad2deg(tmp)
            # print(angle)
            if angle >= 120:
                temp_key_pixels.remove(i)
                bend_pixels.append(i)
    key_pixels = temp_key_pixels
    k = 0
    for i in vector_points:
        # Рисование
        # draw_by_xy(i, h, w, "images/vectors/" + filename + '_' + str(k) + "_vectors.png")
        k += 1

    # print(key_pixels)

    # Рисование
    # if len(key_pixels) != 0:
    # draw_by_xy(key_pixels, h, w, "images/key/" + filename + "_key_pixels.png")

    black_pixels = xy_from_matrix(bin_pixels, h, w)
    # print("Black pixels are: ", black_pixels)
    # print("Key pixels are: ", key_pixels)
    # print("Bend pixels are: ", bend_pixels)

    # Ищем ребра волновым алгоритмом
    # print("Lee algorithm is: ")

    start_points = key_pixels + bend_pixels

    temp_key_pixels = []

    for i in lee_algorithm(start_points, black_pixels):
        temp_key_pixels.append(list(map(lambda _: _.coord, i)))
        # print(temp_key_pixels[-1])

    edges = []

    for i in temp_key_pixels:
        if not (i[::-1] in edges or i in edges):
            edges.append(i)

    # print('Edges are:')
    r = 0
    for i in edges:
        # print(i)
        # Рисование
        # draw_by_xy(i, h, w, 'images/edges/' + str(r) + '_' + filename + '.png')
        r += 1

    # Ищем коэффициенты изгиба
    coefficient = []

    for i in edges:
        x1 = i[0][0]
        x2 = i[-1][0]
        y1 = i[0][1]
        y2 = i[-1][1]
        d = sp.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        p = full_len(i) / d
        coefficient.append(p)

    # print('Coefficients are:')
    # print(coefficient)

    vectors = []

    for i in range(len(edges)):
        vector = np.array((0., 0.))
        for t in range(len(edges[i]) - 1):
            j = np.array(edges[i][t])
            k = np.array(edges[i][t + 1])
            vector += (k - j) * 2 ** -t
        vectors.append(vector)

    # print('Vectors are:')
    # print(vectors)

    P_list = []
    S_list = []
    O_list = []
    ellipses = []
    for i in range(len(edges)):
        # Геометрия
        if coefficient[i] >= 1.1 or len(edges[i]) < 5 or func.three_in_a_row(edges[i][:3] + edges[i][:-3:-1]):
            func.approximation(edges, vectors, i, P_list, S_list, O_list)
        # Эллипсы и матан
        else:
            if len(edges[i]) >= 5:
                vector_a = [edges[i][0], edges[i][len(edges[i]) // 4], edges[i][len(edges[i]) // 2],
                            edges[i][len(edges[i]) // 4 * 3], edges[i][-1]]
                # matrix_D = []
                # for x, y in vector_a:
                #     matrix_D.append([x ** 2, x * y, y ** 2, x, y, 1])
                # matrix_D = np.array(matrix_D)
                # matrix_S = np.dot(matrix_D.T, matrix_D)
                # matrix_C = np.zeros((6, 6))
                # matrix_C[0, 2] = 2
                # matrix_C[2, 0] = 2
                # matrix_C[1, 1] = -1
                # E_vector, V = np.linalg.eig(np.dot(np.linalg.inv(matrix_S), matrix_C))
                #
                # max_V = V[:, np.argmax(np.abs(E_vector))]
                max_V = fivePointsToConic(np.array(vector_a))
                if max_V[1] ** 2 / 4 - max_V[0] * max_V[2] < 0:
                    # print('ELLIPSIS::')
                    # print(coefficient[i], vector_a, max_V)
                    # print('::')
                    ellipses.append(MyEllipsis(max_V))
                    ellipses[-1].set_interval(edges[i][0], edges[i][-1], edges[i][len(edges[i]) // 2])
                else:
                    func.approximation(edges, vectors, i, P_list, S_list, O_list)

    OPS_points = list(zip(O_list, P_list, S_list))

    line = []
    x = step
    y = step
    while x < w:
        line.append([Line(1, A=1, B=0, C=-x)])
        x += step
    while y < h:
        line.append([Line(1, A=0, B=1, C=-y)])
        y += step

    for it in line:
        A, B, C = it[0].A, it[0].B, it[0].C
        it.append(0)
        for ell in ellipses:
            it[-1] += ell.crossings(A, B, C)
        for O, P, S in OPS_points:
            if func.intersection_line_segment(A, B, C, O, P):
                it[-1] += 1
            if func.intersection_line_segment(A, B, C, P, S):
                it[-1] += 1

    segments = [[O, P] for O, P, _ in OPS_points] + [[S, P] for _, P, S in OPS_points]

    ellipses_dict = list(map(lambda _: _.as_dict(), ellipses))
    lines_dict = list(map(lambda _: _[0].as_dict(), line))

    # # print(key_pixels)

    #PlotModel(segments=segments, arcs=ellipses_dict, keyPoints=key_pixels,
    #          lines=lines_dict, intersections=[])
    return list(map(lambda _: _[-1], line))

lol_kek("1")

# references = [Reference(_) for _ in range(10)]
#
# for count in range(10):
#         filenames = os.listdir('./images/original/' + str(count))
#         for fn in filenames[:-2]:
#             try:
#                 print('./images/original/%d/' % count + fn)
#                 references[count].add_reference(lol_kek('./images/original/%d/' % count + fn))
#             except TypeError:
#                 continue
#
#         outp = open('./references/' + str(count), 'w')
#         [outp.write(str(_) + '\n') for _ in references[count].references]
#         outp.close()

# print([])
