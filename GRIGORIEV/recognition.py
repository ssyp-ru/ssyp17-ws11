import os
from main import lol_kek
import func
import numpy as np

img = './images/original/0/2527'

for i in range(10):
    print(open('./references/%d' % i).read().split('\n'))
    # references = list(map(lambda _: list(_), open('./references/%d' % i).read().split('\n')))
    # print(references)
