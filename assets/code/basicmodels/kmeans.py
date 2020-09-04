import numpy as np
import tensorflow as tf
from tensorflow.contrib.factorization import KMeans

# ignore all gpus, tf k-means does not benefit from it
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)
full_data_x = mnist.train.images

# parameters
num_steps = 50  # total steps to train
batch_size = 1024  # the number of samples per batch
k = 25  # the number of clusters
num_classes = 10  # the 10 digits
num_features = 784

# input images
X = tf.placeholder(tf.float32, shape=[None, num_features])
# labels
Y = tf.placeholder(tf.float32, shape=[None, num_classes])

# k-means parameters
kmeans = KMeans(inputs=X, num_clusters=k, distance_metric='cosine', use_mini_batch=True)

# build kmeans graph
training_graph = kmeans.training_graph()
print(len(training_graph))
if len(training_graph) > 6:
    (all_scores, cluster_idx, scores, cluster_centers_initialized,
     cluster_centers_var, init_op, train_op) = training_graph
else:
    (all_scores, cluster_idx, scores, cluster_centers_initialized, init_op, train_op) = training_graph

cluster_idx = cluster_idx[0]
avg_distance = tf.reduce_mean(scores)

# initialize the variables
init_vars = tf.global_variables_initializer()

# start tf session
sess = tf.Session()

# run the initializer
sess.run(init_vars, feed_dict={X: full_data_x})
sess.run(init_op, feed_dict={X: full_data_x})

# training
for i in range(1, num_steps + 1):
    _, d, idx = sess.run([train_op, avg_distance, cluster_idx], feed_dict={X: full_data_x})
    if i % 10 == 0 or i == 1:
        print("Step %i, Avg distance: %f " % (i, d))

    # assign a label to each centroid
    # count total number of labels per centroid, using the label of each training
    # sample to their closest centroid (given by 'idx')
    counts = np.zeros(shape=(k, num_classes))
    for i in range(len(idx)):
        counts[idx[i]] += mnist.train.labels[i]

    # assign the most frequent label to the centroid
    labels_map = [np.argmax(c) for c in counts]
    labels_map = tf.convert_to_tensor(labels_map)

    # evaluation ops
    # lookup: centroid_id -> label
    cluster_label = tf.nn.embedding_lookup(labels_map, cluster_idx)
    # computer accuracy
    correct_pred = tf.equal(cluster_label, tf.cast(tf.argmax(Y, 1), tf.int32))
    accuracy_op = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    # test models
    test_x, test_y = mnist.test.images, mnist.test.labels
    print("test accuracy: ", sess.run(accuracy_op, feed_dict={X: test_x, Y :test_y}))