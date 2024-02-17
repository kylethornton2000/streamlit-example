import numpy as np
import random
from typing import List, Dict, Tuple, Callable
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

# num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
# num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

def parse_data(file_name: str) -> List[List]:
    data = []
    file = open(file_name, "r")
    for line in file:
        datum = [float(value) for value in line.rstrip().split(",")]
        data.append(datum)
    random.shuffle(data)
    return data
def create_folds(xs: List, n: int) -> List[List[List]]:
    k, m = divmod(len(xs), n)
    # be careful of generators...
    return list(xs[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
def create_train_test(folds: List[List[List]], index: int) -> Tuple[List[List], List[List]]:
    training = []
    test = []
    for i, fold in enumerate(folds):
        if i == index:
            test = fold
        else:
            training = training + fold
    return training, test
def processing(nearest):
    sum = 0
    for item in nearest:
        sum += item[1][-1]
    sum = sum/len(nearest)
    return sum
def knn(dataset, query, k):
    distances = []
    for item in dataset:
        distance = 0
        for index,feature in enumerate(item):
            if index == len(item)-1:
                continue
            distance += (query[index]-feature)**2
        distance = distance**.5
        distances.append((distance,item))
    distances = sorted(distances,key = lambda sort: sort[0])
    nearest = distances[:k]
    return processing(nearest)


data = parse_data("concrete_compressive_strength.csv")
folds = create_folds(data, 10)
train, test = create_train_test(folds, 0)
st.line_chart(data)


