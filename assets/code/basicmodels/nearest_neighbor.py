import numpy as np
import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

# limit mnist data
Xtr, Ytr = mnist.train.next_batch(5000) # 5000 for training (nn candidates)
Xte, Yte = mnist.test.next_batch(200) # 200 for test

# tf graph input
xtr = tf.placeholder("float", [None, 784])
xte = tf.placeholder("float", [784])

# nearest neighbor calculation using L1 distance
# calculate l1 distance
distance = tf.reduce_sum(tf.abs(tf.add(xtr, tf.negative(xte))), reduction_indices=1)
# prediction: get min distance index (nearest neighbor)
prediction = tf.arg_min(distance, 0)

accuracy = 0

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    # loop over test data
    for i in range(len(Xte)):
        # get nearest neighbor
        nn_index = sess.run(prediction, feed_dict={xtr: Xtr, xte: Xte[i, :]})
        # get nearest neighbor class label and compare it to its true label
        print("Test", i , "Prediction: ", np.argmax(Ytr[nn_index]), "True class: ", np.argmax(Yte[i]))
        # calculate accuracy
        if np.argmax(Ytr[nn_index]) == np.argmax(Yte[i]):
            accuracy += 1./len(Xte)
    print("Done! ")
    print("Accuracy: ", accuracy)
