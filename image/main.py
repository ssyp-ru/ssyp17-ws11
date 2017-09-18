#from PIL import Image
import numpy as np
from matplotlib import image
import scipy.misc
from libImage import *
import random

fn = input("Введите имя файла без расширения: ")
filename = "/home/ilya/картинки/" + fn + ".png"
pixels, w, h = openimage(filename)
gist = creategist(pixels, w, h)
print("Гистограмма:")
print(gist)
pixels, index = binarize(pixels, gist, w, h)
print("Индекс: " + str(index))
image.imsave("/home/ilya/картинки/" + fn + ".black.png", pixels, 0, 255, cmap="gray", origin="upper")
pixels = skeleton1(pixels, w, h)
image.imsave("/home/ilya/картинки/" + fn + ".skelet1.png", pixels, 0, 255, cmap="gray", origin="upper")
pixels = skeleton2(pixels, w, h)
image.imsave("/home/ilya/картинки/" + fn + ".skelet2.png", pixels, 0, 255, cmap="gray", origin="upper")
keypix = key1(pixels, w, h)
image.imsave("/home/ilya/картинки/" + fn + ".key1.png", keypix, 0, 255, cmap="gray", origin="upper")
keypix = key2(keypix, w, h)
image.imsave("/home/ilya/картинки/" + fn + ".key2.png", keypix, 0, 255, cmap="gray", origin="upper")
allarr = separateKeyPix(pixels, keypix, w, h)
rgb = [[0 for _ in range(w)] for __ in range(h)]
for i in range(h):
    for j in range(w):
        if allarr[i][j] == 1:
            rgb[i][j] = [0, 0, 0]
        elif allarr[i][j] == 2:
            rgb[i][j] = [0, 255, 0]
        elif allarr[i][j] == 3:
            rgb[i][j] = [255, 0, 0]
        else:
            rgb[i][j] = [255, 255, 255]

scipy.misc.toimage(rgb, cmin=0, cmax=255).save("/home/ilya/картинки/" + fn + ".key3.png")
pass

tempallarr = allarr.__deepcopy__(allarr)
listedges = []

for i in range(h):
    for j in range(w):
        if tempallarr[i, j] != 3:
            continue
        neigh = findBlack(tempallarr, i, j)
        templine = []
        templine.append((i, j))
        templine.append(neigh[0])
        templine = findLine(tempallarr, templine, delete = True)
        templine=templine[::-1]
        startPoint=templine[-1]
        prevPoint=templine[-2]
        edge = []
        line = {"coords": templine, "vectors": [], "cf": 0}
        edge.append(line)
        isb=True
        while isb:
            templine = []
            templine.append(startPoint)
            neigh = findBlack(allarr, templine[-1][0], templine[-1][1])
            templine.append(neigh[0] if neigh[0] != prevPoint else neigh[1])
            templine=findLine(allarr, templine)
            startPoint = templine[-1]
            prevPoint = templine[-2]
            if allarr[templine[-1][0]][templine[-1][1]] == 2:
                isb = False
            line = {"coords": templine, "vectors": [], "cf": 0}
            edge.append(line)
        listedges.append(edge)
        '''line = []
        line.append([])
        line.append([])
        line[0].append((i, j))
        line[0].append(neigh[0])
        line[1].append((i, j))
        line[1].append(neigh[1])
        line[0] = findLine(allarr, line[0], delete = True)
        line[1] = findLine(allarr, line[1], delete = True)
        line[0] = line[0][:: - 1]
        for it in range(1,len(line[1])):
            line[0].append(line[1][it])
        listofcompositeedges.append(line[0])'''
for edg in listedges:
    colors = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
    for lns in edg:
        for ed in lns["coords"]:
            if rgb[ed[0]][ed[1]] == [0, 0, 0]:
                rgb[ed[0]][ed[1]] = colors
scipy.misc.toimage(rgb, cmin=0, cmax=255).save("/home/ilya/картинки/" + fn + ".edge.png")

for edge in listedges:
    for ln in edge:
        ln["cf"] = len(ln["coords"]) / np.sqrt(((ln["coords"][0][0] - ln["coords"][-1][0]) ** 2) + ((ln["coords"][0][1] - ln["coords"][-1][1]) ** 2))
        vectors = []
        vectors.append(findVectors(ln["coords"]))
        vectors.append(findVectors(ln["coords"][::-1]))
        ln["vectors"].append(calculateVectors(vectors[0]))
        ln["vectors"].append(calculateVectors(vectors[1]))

pass

