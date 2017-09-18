import pandas as pd
import numpy as np


def read_csv_file(filename):
    data = pd.read_csv(filename)
    # print(data)
    return data


def convert_to_important_data_custom(data_csv):
    cols = ['price', 'bedrooms', 'bathrooms', 'floors', 'waterfront', 'view', 'condition',
                            'sqft_living', 'sqft_lot']
    np_arr_of_data = np.array(data_csv[cols])
    # маштабирование
    np_arr_of_data[:, 7] *= 0.00001
    np_arr_of_data[:, 8] *= 0.00001
    return np_arr_of_data


def get_price(converted_data):
    return np.array(converted_data[:, 0])
