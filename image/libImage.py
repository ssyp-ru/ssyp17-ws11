from PIL import Image
import numpy as np

WHITE = 255
BLACK = 0
GREY = 100
X = 2
Y = 3
C = 2


def color(p):
    for i in range(len(p)):
        if p[i] == 255:
            p[i] = 0
        else:
            p[i] = 1
    return p


def color2(p, w, h):
    for i in range(h):
        for j in range(w):
            if p[i, j] == 255:
                p[i, j] = 0
            else:
                p[i, j] = 1
    return p


def checkTables(tbl, piece, needMod):
    ys = 0
    ones = 0
    matches = 0
    havey = False
    for c in range(len(tbl)):
        if tbl[c] == X:
            continue
        if tbl[c] == Y:
            ys += 1
            havey = True
            continue
        if tbl[c] != piece[c]:
            ones += 1
        else:
            ones += 1
            matches += 1
    if (ones == matches) and ((not havey) or (ys > 0)):
        needMod = True
        return needMod
    return needMod


def skeleton1(pixels, w, h):
    print("Начало 1 стадии скелетизации")
    wasMod = [True, True]
    iter = 1
    while wasMod[0] or wasMod[1]:
        mod = pixels.__deepcopy__(pixels)
        wasMod[iter % 2] = False
        for i in range(1, h - 1):
            for j in range(1, w - 1):
                if (pixels[i, j] == WHITE):
                    continue
                piece = color(
                    [pixels[i - 1, j], pixels[i - 1, j + 1], pixels[i, j + 1], pixels[i + 1, j + 1], pixels[i + 1, j], pixels[i + 1, j - 1], pixels[i, j - 1], pixels[i - 1, j - 1]])
                st1 = (sum(piece))
                if (st1 > 6 or st1 < 2):
                    continue
                a = "".join([str(x) for x in piece])
                a += str(piece[0])
                if (a.count("01") != 1):
                    continue
                if (iter % 2 == 1):
                    if (piece[0] == 1 and piece[2] == 1 and piece[4] == 1):
                        continue
                    if (piece[2] == 1 and piece[4] == 1 and piece[6] == 1):
                        continue
                if (iter % 2 == 0):
                    if (piece[0] == 1 and piece[2] == 1 and piece[6] == 1):
                        continue
                    if (piece[0] == 1 and piece[4] == 1 and piece[6] == 1):
                        continue
                mod[i, j] = WHITE
                wasMod[iter % 2] = True
        pixels = mod
        print(iter)
        # sn=toStr(i)
        # image.imsave("/home/ilya/картинки/slide/" + sn + ".png", pixels, 0, 255, cmap="gray", origin="upper")
        iter += 1
    print("Готово")
    return pixels


def skeleton2(pixels, w, h):
    print("Начало 2 стадии скелетизации")
    wasMod = True
    iter = 1
    while (wasMod):
        wasMod = False
        tables = [
            [1, Y, 0, Y, 1, 1, 1, 1],
            [1, 1, 1, Y, 0, Y, 1, 1],
            [1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, X, 1, X, 1, X],
            [1, X, 0, 0, 0, X, 1, X],
            [1, 1, 1, X, 0, 0, 0, X],
            [0, X, 1, 1, 1, X, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 1, 1, 1, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 1],
            [0, 1, 1, 1, 0, 0, 0, 0]
        ]
        table43 = [Y, 1, 1, X, 0, 1, 1, Y, 1, 1, X]
        table34 = [Y, 0, Y, 1, 1, 1, 1, 1, X, 1, X]
        for i in range(1, h - 2):
            for j in range(1, w - 2):
                if (pixels[i, j] == WHITE):
                    continue
                needMod = False
                piece3x3 = color([pixels[i - 1, j], pixels[i - 1, j + 1], pixels[i, j + 1], pixels[i + 1, j + 1], pixels[i + 1, j], pixels[i + 1, j - 1], pixels[i, j - 1], pixels[i - 1, j - 1]])
                piece43 = color([pixels[i - 1, j - 1], pixels[i - 1, j], pixels[i - 1, j + 1], pixels[i - 1, j + 2], pixels[i, j - 1], pixels[i, j + 1], pixels[i, j + 2], pixels[i + 1, j - 1], pixels[i + 1, j], pixels[i + 1, j + 1], pixels[i + 1, j + 2]])
                piece34 = color([pixels[i - 1, j - 1], pixels[i - 1, j], pixels[i - 1, j + 1], pixels[i, j - 1], pixels[i, j + 1], pixels[i + 1, j - 1], pixels[i + 1, j], pixels[i + 1, j + 1], pixels[i + 2, j - 1], pixels[i + 2, j], pixels[i + 2, j + 1]])
                for tbl in tables:
                    needMod = checkTables(tbl, piece3x3, needMod)
                needMod = checkTables(table43, piece43, needMod)
                needMod = checkTables(table34, piece34, needMod)
                if (needMod):
                    wasMod = True
                    pixels[i, j] = WHITE
        print(iter)
        iter += 1
    print("Готово")
    return pixels


def key1(pixels, w, h):
    print("Выделение ключевых точек", end="")
    keypix = [[WHITE for _ in range(w)] for __ in range(h)]
    keypix = np.array(keypix)
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            #print("\t", i, j)
            pxls = color2(pixels.__deepcopy__(pixels), w, h)
            if (pxls[i, j] == 0):
                continue
            if (sum([pxls[i - 1, j], pxls[i - 1, j + 1], pxls[i, j + 1], pxls[i + 1, j + 1], pxls[i + 1, j], pxls[i + 1, j - 1], pxls[i, j - 1], pxls[i - 1, j - 1]]) != 2):
                keypix[i, j] = BLACK
                continue
            # a group
            if (pxls[i - 1, j + 1] == 1 and pxls[i + 1, j + 1] == 1):
                keypix[i, j] = BLACK
                continue
            if (pxls[i + 1, j - 1] == 1 and pxls[i + 1, j + 1] == 1):
                keypix[i, j] = BLACK
                continue
            if (pxls[i - 1, j - 1] == 1 and pxls[i + 1, j - 1] == 1):
                keypix[i, j] = BLACK
                continue
            if (pxls[i - 1, j - 1] == 1 and pxls[i - 1, j + 1] == 1):
                keypix[i, j] = BLACK
                continue
            # b group
            if ((pxls[i - 1, j] == 1 and pxls[i + 1, j + 1] == 1) and (pxls[i, j + 2] == 1 or pxls[i + 1, j + 2] == 1)):
                keypix[i, j] = BLACK
                continue
            if ((pxls[i + 1, j - 1] == 1 and pxls[i, j + 1] == 1) and (pxls[i - 2, j - 1] == 1 or pxls[i - 2, j] == 1)):
                keypix[i, j] = BLACK
                continue
            if ((pxls[i - 1, j] == 1 and pxls[i + 1, j - 1] == 1) and (pxls[i, j - 2] == 1 or pxls[i + 1, j - 2] == 1)):
                keypix[i, j] = BLACK
                continue
            if ((pxls[i - 1, j + 1] == 1 and pxls[i + 1, j] == 1) and (pxls[i - 1, j + 2] == 1 or pxls[i, j + 2] == 1)):
                keypix[i, j] = BLACK
                continue
            if ((pxls[i - 1, j - 1] == 1 and pxls[i, j + 1] == 1) and (pxls[i - 2, j - 1] == 1 or pxls[i - 2, j] == 1)):
                keypix[i, j] = BLACK
                continue
            if ((pxls[i, j - 1] == 1 and pxls[i - 1, j + 1] == 1) and (pxls[i - 2, j] == 1 or pxls[i - 2, j + 1] == 1)):
                keypix[i, j] = BLACK
                continue
            if ((pxls[i - 1, j - 1] == 1 and pxls[i + 1, j] == 1) and (pxls[i - 1, j - 2] == 1 or pxls[i, j - 2] == 1)):
                keypix[i, j] = BLACK
                continue
            if ((pxls[i, j - 1] == 1 and pxls[i + 1, j + 1] == 1) and (pxls[i + 2, j] == 1 or pxls[i + 2, j + 1] == 1)):
                keypix[i, j] = BLACK
                continue
            # y group
            if ((pxls[i - 1, j - 1] == 1 and pxls[i + 1, j + 1] == 1) and (pxls[i - 2, j] == 1 or pxls[i, j - 2] == 1) and (pxls[i, j + 2] == 1 or pxls[i + 2, j] == 1)):
                keypix[i, j] = BLACK
                continue
            if ((pxls[i - 1, j + 1] == 1 and pxls[i + 1, j - 1] == 1) and (pxls[i + 2, j] == 1 or pxls[i, j - 2] == 1) and (pxls[i, j + 2] == 1 or pxls[i - 2, j] == 1)):
                keypix[i, j] = BLACK
                continue
    print("...OK")
    return keypix


def key2(pixels, w, h):
    print("Объединение ключевых точек", end="")
    wasMod = True
    while (wasMod):
        wasMod = False
        for i in range(1, h - 1):
            for j in range(1, w - 1):
                if pixels[i, j] == WHITE:
                    continue
                piece = color([pixels[i - 1, j], pixels[i - 1, j + 1], pixels[i, j + 1], pixels[i + 1, j + 1], pixels[i + 1, j], pixels[i + 1, j - 1], pixels[i, j - 1], pixels[i - 1, j - 1], pixels[i - 1, j]])
                a = "".join([str(x) for x in piece])
                if a.count("01") == 1:
                    pixels[i, j] = WHITE
                    wasMod = True
    print("...OK")
    return pixels


def findBlack(arr, i, j, ):
    temp = []
    if (arr[i - 1, j] != 0):
        temp.append((i - 1, j))
    if (arr[i - 1, j + 1] != 0):
        temp.append((i - 1, j + 1))
    if (arr[i, j + 1] != 0):
        temp.append((i, j + 1))
    if (arr[i + 1, j + 1] != 0):
        temp.append((i + 1, j + 1))
    if (arr[i + 1, j] != 0):
        temp.append((i + 1, j))
    if (arr[i + 1, j - 1] != 0):
        temp.append((i + 1, j - 1))
    if (arr[i, j - 1] != 0):
        temp.append((i, j - 1))
    if (arr[i - 1, j - 1] != 0):
        temp.append((i - 1, j - 1))
    return temp


def findLine(arr, line, it = 0, delete = False):
    #TODO Проверить поиск точек
    i, j = line[-1]
    neigh = findBlack(arr, i, j)
    '''if ((arr[i, j] == 3) or (arr[neigh[0]]) or ()) and delete:
        arr[i, j] = 1'''
    if delete:
        if arr[i, j] == 3:
            arr[i, j] =1
        elif arr[neigh[0]] == 3:
            arr[neigh[0]] = 1
        elif arr[neigh[1]] == 3:
            arr[neigh[1]] = 1
    for n in neigh:
        if (arr[n] > 1 and it > 0):
            line.append(n)
            return line
    it += 1
    if (arr[i, j] != 1):
        return line
    else:
        if (neigh[0] == line[-2]):
            line.append(neigh[1])
            line = findLine(arr, line, it, delete = delete)
        else:
            line.append(neigh[0])
            line = findLine(arr, line, it, delete = delete)
    return line


def findVectors(line):
    vectors = []
    for it in range(1, len(line)):
        i = line[it][0] - line[0][0]
        j = line[it][1] - line[0][1]
        vectors.append((i, j))
    return vectors


def calculateVectors(vectors):
    crt = [0, 0]
    for it in range(len(vectors)):
        i = vectors[it][0]
        j = vectors[it][1]
        crt[0] += i * (2 ** (-it))
        crt[1] += j * (2 ** (-it))

    return tuple(crt)


def separateKeyPix(pixels, keypix, w, h):
    print("Поиск точек изгиба:")
    allarr = np.copy(color2(pixels, w, h))
    kp = color2(keypix, w, h)
    for i in range(h):
        for j in range(w):
            allarr[i, j] += kp[i, j]
    for i in range(h):
        for j in range(w):
            if (allarr[i, j] != 2):
                continue
            piece = [pixels[i - 1, j], pixels[i - 1, j + 1], pixels[i, j + 1], pixels[i + 1, j + 1], pixels[i + 1, j], pixels[i + 1, j - 1], pixels[i, j - 1], pixels[i - 1, j - 1]]
            if (sum(piece) == 2):
                allarr[i, j] += 1

    for i in range(h):
        for j in range(w):
            if (allarr[i, j] != 3):
                continue
            line = []
            line.append([])
            line.append([])
            vector = []
            finalVector = []
            neigh = findBlack(allarr, i, j)
            line[0].append((i, j))
            line[0].append(neigh[0])
            line[1].append((i, j))
            line[1].append(neigh[1])
            line[0] = findLine(allarr, line[0])
            line[1] = findLine(allarr, line[1])
            vector.append(findVectors(line[0]))
            vector.append(findVectors(line[1]))
            finalVector.append(calculateVectors(vector[0]))
            finalVector.append(calculateVectors(vector[1]))
            print(finalVector)
            m = finalVector[0][0]
            n = finalVector[0][1]
            k = finalVector[1][0]
            l = finalVector[1][1]
            cs = ((m * k) + (n * l)) / ((np.sqrt((m ** 2) + (n ** 2))) * (np.sqrt((m ** 2) + (n ** 2))))
            angle = np.arccos(cs)
            angle = np.rad2deg(angle)
            print(angle)
            if (angle < 120):
                allarr[i, j] = 2
    print("Готово")
    return allarr


def openimage(filename):
    img = Image.open(filename).convert("L")
    w, h = img.size
    print("Разрешение " + str(w) + "*" + str(h) + " пикселей")
    pixels = img.load()
    pixels = np.reshape([pixels[i, j] for j in range(h) for i in range(w)], (h, w))
    return pixels, w, h


def creategist(pixels, w, h):
    gist = [0 for _ in range(256)]
    for j in range(w):
        for i in range(h):
            gist[pixels[i, j]] += 1
    return gist


def binarize(pixels, gist, w, h):
    print("Начало бинаризации", end='')
    n = sum(gist)
    m = sum([t * gist[t] for t in range(256)])
    res = 0
    index = 0
    b = 0
    a = 0
    for i in range(0, 256):
        b += gist[i]
        a += i * gist[i]
        if (b == 0 or n == b):
            continue
        v1 = b / n
        v2 = 1 - v1
        m1 = a / b
        m2 = (m - a) / (n - b)
        temp = v1 * v2 * ((m1 - m2) ** 2)
        if (temp > res):
            res = temp
            index = i
    pixels[pixels >= index] = 255
    pixels[pixels < index] = 0
    print("...OK")
    return pixels, index
