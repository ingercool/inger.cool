import tensorflow as tf
# import mnist data
import tensorflow.examples.tutorials.mnist.input_data as input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

# parameters
learning_rate = 0.01
training_epochs = 25
batch_size = 100
display_step = 1

# tf graph input
x = tf.placeholder(tf.float32, [None, 784]) # mnist data image of shape 28*28 = 784
y = tf.placeholder(tf.float32, [None, 10]) # 0-9 digits recognition => 10 classes

# set model weights
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))

# construct model
prediction = tf.nn.softmax(tf.matmul(x,W) + b) # softmax

# minimize error using error entropy
cost = tf.reduce_mean(-tf.reduce_sum(y*tf.log(prediction), reduction_indices=1))
# gradient descent
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# initialize the variables
init = tf.global_variables_initializer()

with tf.Session() as sess:
    # run the initializer
    sess.run(init)

    # training cycle
    for epoch in range(training_epochs):
        avg_cost = 0
        total_batch = int(mnist.train.num_examples/batch_size)

        # loop over all batches
        for i in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            # run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_xs, y: batch_ys})

            # compute average loss
            avg_cost += c/total_batch

        # display logs per epoch step
        if(epoch+1) % display_step == 0:
            print("epoch: ", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost))

    print("optimization finished")

    # test model
    correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
    # calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print("accuracy: ", accuracy.eval({x:mnist.test.images, y:mnist.test.labels}))