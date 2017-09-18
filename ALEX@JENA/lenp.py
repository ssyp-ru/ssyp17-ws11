import numpy as np
def len_path(put):
    lenght = 0
    (x, y) = put[0]
    put = put[1:len(put) - 1]
    for (m ,k) in put:
        if m != x and k != y:
            lenght += np.sqrt(2)
            print('+sq2')
        else:
            lenght += 1
            print('+1')
        (x, y) = (m, k)
    return lenght

path = [(7, 11), (7, 12), (7, 13), (7, 14), (7, 15), (6, 16), (6, 17), (6, 18), (7, 19)]

len_path(path)