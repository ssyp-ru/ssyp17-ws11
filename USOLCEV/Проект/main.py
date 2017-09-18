from files import *
from ml import *
import numpy as np

data = convert_to_important_data_custom(read_csv_file("kc_house_data.csv"))
price = get_price(data)
data = create_1_colm(data)
data = data[:, 1:]

with open('lr_model.txt', 'r') as f:
    raw_data = f.readlines()
    thetas = np.array([float(x) for x in raw_data[:-2]])
    calc_rate(data, price, thetas, data.shape[0])

# teta_arr = [1 for _ in range(data.shape[1])]
# find_teta(1000, data, 0.0555, np.array(teta_arr, dtype=np.float32), price)
