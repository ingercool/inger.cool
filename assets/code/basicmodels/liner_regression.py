import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

rng = np.random

# parameters
learning_rate = 0.01
tranining_epochs = 1000
display_step = 50

# training data
train_X = np.asarray([3.3, 4.4, 5.5, 6.71, 6.93, 4.168, 9.779, 6.182, 7.59, 2.167, 7.042, 10.791, 5.313, 7.997, 5.564, 9.27, 3.1])
train_Y = np.asarray([1.7, 2.76, 2.09, 3.19, 1.694, 1.573,3.366, 2.596, 2.53, 1.221, 2.827, 3.465, 1.65, 2.904, 2.42, 2.94, 1.3])
n_samples = train_X.shape[0]

# tf graph input
X = tf.placeholder("float")
Y = tf.placeholder("float")

# set model weights
W = tf.Variable(rng.randn(), name="weight")
b = tf.Variable(rng.randn(), name="bias")

# construct a liner model
pred = tf.add(tf.multiply(X,W), b)

# mean squared error
cost = tf.reduce_sum(tf.pow(pred-Y, 2))/(2*n_samples)
# gardient desent
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# initialize the vatiables
init = tf.global_variables_initializer()

# start
with tf.Session() as sess:
    sess.run(init)
    # fit all training data
    for epoch in range(tranining_epochs):
        for(x , y) in zip(train_X, train_Y):
            sess.run(optimizer, feed_dict={X: x, Y : y})
        # display log per epoch step
        if (epoch + 1) % display_step == 0:
            c = sess.run(cost, feed_dict={X : train_X, Y : train_Y})
            print("Epoch:", '%04d' %(epoch+1), " cost = ", "{:.9f}".format(c), "W =", sess.run(W), " b = ", sess.run(b))


    print("optimization finished!")
    training_cost = sess.run(cost, feed_dict={X: train_X, Y : train_Y})
    print("training cost = ", training_cost, "W = ", sess.run(W), " b = ", sess.run(b))

    # graphic display
    plt.plot(train_X, train_Y, 'ro', label = 'original data')
    plt.plot(train_X, sess.run(W) * train_X + sess.run(b), label = 'fitted line')
    for a, b in zip(train_X, train_Y):
        plt.text(a, b, (a,b), ha='center', va='bottom', fontsize=10)
    plt.legend()
    plt.show()

    # # testing example,
    # test_X = np.asarray([6.83, 4.668, 8.9, 7.91, 5.7, 3.1, 2.1])
    # test_Y = np.asarray([1.84, 2.273, 3.2, 2.381, 2.92, 3.24, 1.35, 1.03])
    #
    # print("testing...(mean square loss comparison)")
    # testing_cost = sess.run(
    #     tf.reduce_sum(tf.pow(pred - Y, 2)) / (2 * test_X.shape[0]),
    #     feed_dict={X: test_X, Y: test_Y})
    # print("testing cost = ", testing_cost)
    # print("absolute mean square loss difference: ", abs(training_cost - testing_cost))

    # plt.plot(test_X, test_Y, 'bo', label='testing data')
    # plt.polt(train_X, sess.run(W) * train_X + sess.run(b), label='fitted line')
    # plt.legend()
    # plt.show()