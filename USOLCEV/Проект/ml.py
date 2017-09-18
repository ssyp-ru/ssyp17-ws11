import numpy as np


def create_1_colm(np_arr_of_data):
    return np.concatenate((np_arr_of_data, np.array([[1] for _ in range(np_arr_of_data.shape[0])])), axis=1)


# h0(x)
def np_mult_data(teta,arr_of_data_with):
    return np.dot(teta.T,arr_of_data_with)

# j(0)
# m - кол-во примеров
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#


def J(teta,x,y,size):
    temp_value = 0
    for i in range(size):
        temp_value += (np_mult_data(teta,x[i]) - y[i])**2
    return 1/(2*size) * temp_value

# [:, 1:]
def whatIsIt(size,teta,arr_data,y, j):
    temp_value = 0
    for i in range(size):
        temp_value += (np_mult_data(teta,arr_data[i]) - y[i]) * arr_data[i][j]
    return (1/size) * temp_value
# der j


def find_teta(max_iteration, data, study_step, arr_teta, y):
    temp_arr_teta = []
    if study_step < 0:
        print('StepStudyError!')
        exit(999)
    for _iter in range(max_iteration):
        prev_cost = J(arr_teta, data, y, data.shape[0])
        for j in range(data.shape[1]):
            temp_arr_teta.append(study_step * whatIsIt(data.shape[0], arr_teta, data, y, j))
        for j in range(data.shape[1]):
            arr_teta[j] -= np.array(temp_arr_teta[j], dtype=np.int64)
        cost = J(arr_teta, data, y, data.shape[0])
        print('iteration: {0}\nCost: {1}\ndelta cost: {2}'.format(_iter, cost, prev_cost - cost))

        temp_arr_teta = []
    with open('lr_model.txt', 'w') as f:
        for theta in arr_teta:
            f.write(str(theta) + '\n')
        f.write('\nCost: ' + str(J(arr_teta, data, y, data.shape[0])))

    return arr_teta


def calc_rate(_X, y, thetas, size):
    accum_delta = 0
    for x, y in list(zip(_X, y)):
        accum_delta += np.abs((np_mult_data(thetas, x) - y) / y)
    accum_delta /= size
    print('Error rate: {0} %'.format(int(accum_delta * 10000) / 100))
