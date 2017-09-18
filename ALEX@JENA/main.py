from PIL import Image
import numpy as np
from matplotlib import image as mp
import re, time



start_x = 0
start_y = 0
coef = 1

temp_x = 0
temp_y = 0

usm1 = []
usm2 = []

count = 1
paths = []


bend_cos = []

# переменные, которые используются для вычисления индекса
a = 0
b = 0
maximum = 0
index = 0

# флаги для проверки модификации пикселей в картинке
wasMOD1 = True
wasMOD2 = True
wasMOD_key = True

# данные списки изспользуются для проверки повтора пикселей в
# скелетизации(чтобы пиксели,которые были уже заменены не повторялись)
array_with_l = []
array_with_w = []

# данные списки изспользуются для создания списка кл.точек
array_of_x = []
array_of_y = []

# данные списки изспользуются для нахождения пути
mod_pixels = []
array_of_izgib = []
array_to_remove = []

# сохранение углов
alpha = []


filename = input("Введите название картинки(без расширения) :")

# открываем изображение
img = Image.open(filename + '.png').convert('L')

# загрузка картинки и получение ее размеров
w, l = img.size
pixels = img.load()

# создаем матрицу пикселей
pixels = np.reshape([pixels[i, j] for j in range(l) for i in range(w)], (l, w))
print('Картинка размером:', w, 'на', l)

# гистограмма
gist = [0 for _ in range(256)]
for j in range(w):
    for i in range(l):
        gist[pixels[i, j]] += 1

# суммы для подсчета индекса
sum1 = sum(gist)
sum2 = sum(x * gist[x] for x in range(256))

# считаем индекс для сравнивания
for i in range(1, 256):
    a += (gist[i - 1] * (i - 1))
    b += gist[i - 1]
    if b == 0 or b == sum1:
        continue
    v1 = b / sum1
    v2 = 1 - v1
    m1 = a / b
    m2 = (sum2 - a) / (sum1 - b)

    total = v1 * v2 * ((m1 - m2) ** 2)
    if total > maximum:
        index = i
        maximum = total

# бинаризация изображения
for j in range(w):
    for i in range(l):
        if pixels[i, j] >= index:
            pixels[i, j] = 255
        else:
            pixels[i, j] = 0

# mp.imsave(filename + "_bin.png", pixels, vmin=0, vmax=255, cmap='gray', origin='upper')
print('Бинаризация : ОК')

# функция, которая возвращает для белого цвета 1 , а для черного 0
def one_null(arr, x, y):
    return 0 if arr[x, y] == 255 else 1

# скелетизация первый алгоритм
def skeletisation_1(arr, x, y, f):
    point = 0

    circ = nearest_index(arr, x, y)

    string = str()

    for (m, k) in circ:
        string += str(one_null(arr, m, k))

    string += str(one_null(arr, x - 1, y))
    string1 = re.findall('01', string)

    if len(string1) == 1:
        point += 1
    else:
        return False

    circ = nearest_elem(arr, x , y , False)

    if (sum(circ) // 255 >= 2) and (sum(circ) // 255 <= 6):
        point += 1
    else:
        return False

    if f % 2 == 1:
        if (circ[0] + circ[2] + circ[4] >= 255) and (circ[2] + circ[4] + circ[6] >= 255):
            point += 2
        else:
            return False
    else:
        if (circ[0] + circ[2] + circ[6] >= 255) and (circ[0] + circ[4] + circ[6] >= 255):
            point += 2
        else:
            return False

    if point == 4: return True

# получает ближайшие элементы (их яркости)
def nearest_elem(arr, x, y, circle=True):
    array = []
    array += [arr[x - 1, y], arr[x - 1, y + 1],
              arr[x, y + 1], arr[x + 1, y + 1],
              arr[x + 1, y], arr[x + 1, y - 1],
              arr[x, y - 1], arr[x - 1, y - 1]]

    if (x + 2 != l and x - 1 != 0) and (y - 1 != 0 and y + 2 != w) and circle:
        array += [arr[x, y + 2],     arr[x + 2, y],
                  arr[x, y - 2],     arr[x - 2, y],
                  arr[x - 1, y + 2], arr[x + 1, y + 2],
                  arr[x + 2, y + 1], arr[x + 2, y - 1],
                  arr[x + 1, y - 2], arr[x - 1, y - 2],
                  arr[x - 2, y - 1], arr[x - 2, y + 1]]
    return array

#возвращает индексы блтжайших элементов
def nearest_index(arr, x, y):
    array = []
    array += [(x - 1, y), (x - 1, y + 1),
              (x, y + 1), (x + 1, y + 1),
              (x + 1, y), (x + 1, y - 1),
              (x, y - 1), (x - 1, y - 1)]
    return array

# скелетизация второй алгоритм
def skeletisation_2(arr, x, y):
    array = nearest_elem(arr, x, y)
    if (array[0] + sum(array[4:8]) == 0 and (array[1] + array[3]) >= 255 and array[2] == 255) or \
        (sum(array[0:3]) + sum(array[6:8]) == 0 and (array[3] + array[5]) >= 255 and array[4] == 255) or \
        (sum(array[0:5]) + array[8] == 0 and array[5] + array[7] >= 255 and array[6] == 255) or \
        (sum(array[2:7]) + array[9] == 0 and array[1] + array[7] >= 255 and array[0] == 255) or \
        (sum(array[0:3]) == 255 * 3 and array[4] + array[6] == 0) or \
        (sum(array[0:3]) == 0 and sum(array[4:7]) == 255 * 3) or \
        (sum(array[0:8]) == 255 * 6 and array[0] + array[2] == 0) or \
        (sum(array[2:5]) == 255 * 3 and array[0] + array[6] == 0) or \
        (sum(array[2:5]) == 0 and array[6] + array[7] + array[0] == 255 * 30) or \
        (sum(array[5:8]) + array[0] + array[1] + array[3] == 6 * 255 and sum(array[0:8]) == 6 * 255) or \
        (sum(array[0:3]) + array[6] + array[7] == 5 * 255 and sum(array[0:8]) == 5 * 255) or \
        (sum(array[0:5]) == 5 * 255 and sum(array[0:8]) == 5 * 255) or \
        (sum(array[2:7]) == 5 * 255 and sum(array[0:8]) == 255 * 5) or \
        (sum(array[4:8]) + array[0] == 5 * 255 and sum(array[0:8]) == 5 * 255): return True
    return False

# функция, определяющая пиксель ключевой или нет
def get_key_pixels(pixels, x, y):
    array_of_nearest_elem = nearest_elem(pixels, x, y)
    if (sum(array_of_nearest_elem[0:8]) != 1530): return True
    #a
    if  (array_of_nearest_elem[1] + array_of_nearest_elem[3] == 0) or \
        (array_of_nearest_elem[3] + array_of_nearest_elem[5] == 0) or \
        (array_of_nearest_elem[5] + array_of_nearest_elem[7] == 0) or \
        (array_of_nearest_elem[7] + array_of_nearest_elem[1] == 0): return True
    if x + 2 == l or x - 2 == -1 or y - 2 == -1 or y + 2 == w: return False
    #b
    if  ((array_of_nearest_elem[0] + array_of_nearest_elem[3] == 0) and (array_of_nearest_elem[13] + array_of_nearest_elem[8] <= 255)) or \
        ((array_of_nearest_elem[0] + array_of_nearest_elem[5] == 0) and (array_of_nearest_elem[10] + array_of_nearest_elem[16] <= 255)) or \
        ((array_of_nearest_elem[2] + array_of_nearest_elem[5] == 0) and (array_of_nearest_elem[9] + array_of_nearest_elem[15] <= 255)) or \
        ((array_of_nearest_elem[1] + array_of_nearest_elem[4] == 0) and (array_of_nearest_elem[8] + array_of_nearest_elem[12] <= 255)) or \
        ((array_of_nearest_elem[2] + array_of_nearest_elem[7] == 0) and (array_of_nearest_elem[11] + array_of_nearest_elem[18] <= 255)) or \
        ((array_of_nearest_elem[4] + array_of_nearest_elem[7] == 0) and (array_of_nearest_elem[10] + array_of_nearest_elem[17] <= 255)) or \
        ((array_of_nearest_elem[1] + array_of_nearest_elem[6] == 0) and (array_of_nearest_elem[11] + array_of_nearest_elem[19] <= 255)) or \
        ((array_of_nearest_elem[3] + array_of_nearest_elem[6] == 0) and (array_of_nearest_elem[9] + array_of_nearest_elem[14] <= 255)): return True
    #y
    if  ((array_of_nearest_elem[7] + array_of_nearest_elem[3] == 0) and (array_of_nearest_elem[10] + array_of_nearest_elem[11] <= 255) and (array_of_nearest_elem[8] + array_of_nearest_elem[9] <= 255)) or \
        ((array_of_nearest_elem[1] + array_of_nearest_elem[5] == 0) and (array_of_nearest_elem[9] + array_of_nearest_elem[10] <= 255) and (array_of_nearest_elem[11] + array_of_nearest_elem[8] <= 255)): return True
    return False

# ищет путь от точки возможного изгиба
def search_path(x1, y1, path):
    global mod_pixels
    cir = nearest_index(pixels, x1, y1)
    for m, k in cir:
        if ((pixels[m, k] == 170) or (pixels[m, k] == 85)) and not ((m, k) in mod_pixels):
            path.append((x1, y1))
            paths.append(path)
            return
    for m, k in cir:
        if (pixels[m, k] == 0) and not ((m, k) in mod_pixels):
            path.append((x1, y1))
            mod_pixels.append((x1, y1))
            return search_path(m, k, path)

def search_path_for_edge(x1, y1, path):
    global mod_pixels
    cir = nearest_index(pixels, x1, y1)
    for m, k in cir:
        if (pixels[m, k] == 170) and not ((m, k) in mod_pixels):
            path.append((x1, y1))
            path.append((m,k))
            paths.append(path)
            return
    for m, k in cir:
        if ((pixels[m, k] == 0) or (pixels[m,k] == 85)) and not ((m, k) in mod_pixels):
            path.append((x1, y1))
            mod_pixels.append((x1, y1))
            return search_path_for_edge(m, k, path)

def len_path(put):
    lenght = 0
    (x, y) = put[0]
    put = put[1: -1]

    for (m ,k) in put:
        if m != x and k != y:
            lenght += np.sqrt(2)
        else:
            lenght += 1
        (x, y) = (m, k)
    return lenght

def count_vectors(way):
    start_x = 0
    start_y = 0
    coef = 1

    temp_x = 0
    temp_y = 0

    usm1 = []
    usm2 = []

    count = 1
    for i in range(len(way)):
        if_first = True
        for m, k in way[i]:
            if if_first:
                count = 0
                start_x = m
                start_y = k
                temp_x = 0
                temp_y = 0
                coef = 1
                if_first = False
                count+=1
                continue
            else:
                temp_x += ((m - start_x)*coef)
                temp_y += ((k - start_y)*coef)
                coef = coef/2
                if (count + 1 == len(way[i])):
                    usm1.append(temp_x)
                    usm2.append(temp_y)
                count+=1
    return usm1 , usm2

def count_cos(arr, fg = True):
    arr_cos = []
    count = 1
    lp = True
    for m, k in arr:
        if count % 2 == 1:
            i1 = m
            j1 = k
            d = np.sqrt(m ** 2 + k ** 2)
            lp = False
        else:
            i2 = m
            j2 = k
            r = np.sqrt(m ** 2 + k ** 2)
            lp = True
        if lp:
            if fg:
                arr_cos.append(((i1 * i2) + (j1 * j2)) / (d * r))
            else:
                return ((i1 * i2) + (j1 * j2)) / (d * r)
        count += 1
    return  arr_cos

black = 0

for i in range(0, l):
    for j in range(0, w):
        if pixels[i, j] == 0: black += 1
bl_counter = 0

# цикл для итераций (первый алгоритм)
while wasMOD1:
    wasMOD1 = False
    change_pixel = list(zip(array_with_l, array_with_w))
    for m, k in change_pixel:
        pixels[m, k] = 255
    for j in range(1, w - 1):
        for i in range(1, l - 1):
            if pixels[i, j] == 255:
                continue
            elif skeletisation_1(pixels, i, j, count) and (i, j) not in change_pixel:
                array_with_l.append(i)
                array_with_w.append(j)
                wasMOD1 = True
                bl_counter += 1
    print(count, bl_counter , '/', black)
    count += 1

# mp.imsave(filename + "_scel.png", pixels, vmin=0, vmax=255, cmap='gray', origin='upper')

# цикл для итераций (второй алгоритм)
count = 1
while wasMOD2:
    wasMOD2 = False
    for i in range(2, l - 2):
        for j in range(2, w - 2):
            if pixels[i, j] == 255:
                continue
            elif skeletisation_2(pixels, i, j):
                pixels[i, j] = 255
                wasMOD2 = True
                bl_counter += 1
    print(count, bl_counter, '/', black)
    count += 1

print('Скелетизация: ОК')

# сздание списка кл.точек
for j in range(w):
    for i in range(l):
        if pixels[i, j] == 255:
            continue
        if get_key_pixels(pixels, i, j):
            array_of_x.append(i)
            array_of_y.append(j)

# список кл.точек
array_of_key_elem = list(zip(array_of_x, array_of_y))

# удаление лишних кл.точек
for j in range(w):
    for i in range(l):
        if (i, j) in array_of_key_elem:
            pixels[i, j] = 510
while wasMOD_key:
    wasMOD_key = False
    for i in range(w):
        for j in range(l):
            string2 = ''
            string3 = ''
            if (i, j) in array_of_key_elem:
                array_of_circle = nearest_elem(pixels, i, j, False)
                for m in array_of_circle:
                    string2 += str(int(m / 255))
                string3 = re.findall('12', string2)
                if len(string3) == 1:
                    array_of_key_elem.remove((i, j))
                    pixels[i, j] = 0
                    wasMOD_key = True
            else:
                continue
for j in range(w):
    for i in range(l):
        if (i, j) in array_of_key_elem:
            pixels[i, j] = 170

# цикл для создания списка возможных точек изгиба
for j in range(w):
    for i in range(l):
        if (i, j) in array_of_key_elem:
            temp = nearest_elem(pixels, i, j, False)
            if sum(temp) == 1530:
                array_of_izgib.append((i, j))
                array_of_key_elem.remove((i, j))
                pixels[i, j] = 85

# цикл, который записывает в список список, состоящик из кортежей с точками
for m, k in array_of_izgib:
    for i in range(2):
        search_path(m, k, path=[])
    mod_pixels = []

# счиатет векторы
t_vec, t_vec1 = count_vectors(paths)

fin_vec = list(zip(t_vec , t_vec1))

#считает косинусы
bend_cos = count_cos(fin_vec)

#превращает косинусы в градусы и записывает в список
for i in bend_cos:
    v = np.arccos(i)
    v = np.rad2deg(v)
    alpha.append(v)

#удаление вохможных точек изгиба
count = 0
for m, k in array_of_izgib:
    if alpha[count] < 120:
        pixels[m, k] = 170
        array_to_remove.append((m, k))
    count += 1

    for m, k in array_to_remove:
        array_of_izgib.remove((m, k))
        array_of_key_elem.append((m, k))

print('Углы:',alpha)


paths = []


for m, k in array_of_key_elem:
    temp_near_elem = nearest_elem(pixels , m ,k , False)
    counter_of_black_points = (8 * 255 - sum(temp_near_elem)) // 255
    for i in range(counter_of_black_points):
        search_path_for_edge(m, k, path=[])
    mod_pixels = []


if_composite = False

if_first = True
count = 0


temp_coef_bend = []
paths_for_coef = []
array_of_bend_edge = []


for i in range(len(paths)):
    for m,k in paths[i]:
        if (m, k) in array_of_izgib:
            if_composite = True
        if if_first:
            start_x1 = m
            start_y1 = k
            count = 0
            if_first = False
        if len(paths[i]) == count+1 :
            end_x2 = m
            end_y2 = k
            if_first = True
            if not if_composite:
                temp_coef = len_path(paths[i]) / ((np.sqrt(((end_x2 - start_x1)**2)  + ((end_y2 - start_y1)**2)))-1)
                paths_for_coef.append(paths[i])
                temp_coef_bend.append(temp_coef)
            else:
                array_of_bend_edge.append(paths[i])
        count += 1


coef_bend = list(zip(paths_for_coef , temp_coef_bend))

t_vec , t_vec1 = count_vectors(paths)

fin_vec_edge = list(zip(t_vec , t_vec1))

path_plus_vec  = list(zip(paths , fin_vec_edge))


# удаление повторяющихся путей
temp_array = []


for m , k in path_plus_vec :
    temp_array.append(m)

temp_array_of_start_end = []

for i in temp_array:
    temp_array_of_start_end.append([i[0], i[-1]])


for i in temp_array_of_start_end:
    if i[::-1] in temp_array_of_start_end:
        temp_array_of_start_end.remove(i[::-1])

temp_tuple = []

for i in temp_array_of_start_end:
    temp_tuple.append(tuple(i))



array_to_remove = []

for i in temp_array:
    if  (tuple((i[0], i[-1]))) not in temp_tuple:
        array_to_remove.append(i)


for i in array_to_remove:
    temp_array.remove(i)


array_to_remove = []

for m , k in coef_bend:
    if m  not in temp_array:
        array_to_remove.append((m,k))

for m,k in array_to_remove:
    coef_bend.remove((m,k))

array_to_remove = []

for m, k in path_plus_vec :
    if m not in temp_array:
        array_to_remove.append((m, k))

for m,k in array_to_remove:
    path_plus_vec.remove((m,k))

n = True
arr_of_line = []

kosil = 0

for (m,k) in coef_bend:
    if k < 1.1 or len(m)<5:
        a = 0
        b = 0
        len_m = len_path(m)
        for z1 , z2 in m:
            if n:
                start_x1 = z1
                start_y1 = z2
                count = 0
                n = False
            if len(m) == count + 1:
                end_x2 = z1
                end_y2 = z2
                n = True
                c = np.sqrt(((end_x2 - start_x1)**2)  + ((end_y2 - start_y1)**2))
                print(c)
                print(len_m)
                (x, vec1) = path_plus_vec[kosil]
                vec2 = ((end_x2 - start_x1), (end_y2 - start_y1))
                cosinus = count_cos([vec1, vec2], False)
                print(cosinus)
                a = (c**2 - len_m**2)/(2*(c*cosinus - len_m))
                print(a)
                b = len_m - a
                print(b)
            count += 1
        arr_of_line.append(((start_x1, start_y1), (end_x2, end_y2), a, b))
    kosil += 1

print(arr_of_line)
# сохраняем конечное изображение
mp.imsave(filename + "_new.png", pixels, vmin=0, vmax=255, cmap='gray', origin='upper')