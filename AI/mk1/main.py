import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.utils import np_utils


text=(open("temp.txt"))


text = " ".join(text).lower()
characters = sorted(list(set(text)))
print(characters)
n_to_char = {n:char for n, char in enumerate(characters)}
char_to_n = {char:n for n, char in enumerate(characters)}

x = []

y = []

length = len(text)
seq_length = 100 #batch size?
for i in range(0,length-seq_length, 1):
    sequence = text[i:i+seq_length]
    label = text[i+seq_length]
    x.append([char_to_n[char] for char in sequence])
    y.append(char_to_n[label])


