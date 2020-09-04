import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

tf.set_random_seed(1)
np.random.seed(1)

# fake data
n_data = np.ones((100,2))
x0 = np.random.normal(2*n_data, 1) # class0 x shape = (100,2)
y0 = np.zeros(100) # class0 y shape = (100, )
x1 = np.random.normal(-2*n_data, 1) # class1 x shape = (100, 2)
y1 = np.ones(100)
