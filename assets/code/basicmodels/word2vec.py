# word to vector : 文本向量化
# input : ont hot vector (only consists by 0 or 1)

import collections
import os
import random
import urllib
import zipfile

import numpy as np
import  tensorflow as tf

# training parameters
learning_rate = 0.1
batch_size = 120
num_steps = 3000000
display_steps = 10000
eval_step = 200000

# evaluation parameters
eval_words = ['five', 'of', 'going', 'hardware', 'chinese', 'britain']

# word2vec parameters
embedding_size = 200  # dimension of the embedding vector
max_vocabulary_size = 50000  # total number of different words in the vocabulary
min_occurrence = 10  # remove all words that does not appears at least n times
skip_window = 3  # how many words to consider left and right
num_skips = 2  # how many times to reuse an input to generate a label
num_sampled = 64  # number of negative examples to sample

# download a small chunk of wikipedia articles collection
url = 'http://mattmahoney.net/dc/text8.zip'
data_path = 'text8.zip'
if not os.path.exists(data_path):
    print("downloading the dataset ... it may take some time")
    filename, _ =urllib.request.urlretrieve(url, data_path)
    print("done!")

# unzip the data set file. text has already been processed
with zipfile.ZipFile(data_path) as f:
    text_words = f.read(f.namelist()[0].lower().split())

# build the dictionary and replace rare words with UNK token
count = [('UNK', -1)]
# retrieve the most common words
count.extend(collections.Counter(text_words).most_common(max_vocabulary_size - 1))
# remove samples with less than 'min_occurrence' occurrences
for i in range(len(count) - 1, -1 , -1):
    if count[i][1] < min_occurrence:
        count.pop(i)
    else:
        # the collection is orded, so stop when 'min_occurrence'
        break
# compute the vocabulary size
vocabulary_size = len(count)
# assign an id to each word
word2id = dict()
for i, (word, _) in enumerate(count):
    word2id[word] = i

data = list()
unk_count = 0
for word in text_words:
    # retrieve a word id, or assign it index 0 if not in dictionary
    index = word2id.get(word, 0)
    if index == 0:
        unk_count += 1
    data.append(index)

count[0] = ('UNK', unk_count)
id2word = dict(zip(word2id.values(), word2id.keys()))

print("words count: ", len(text_words))
print("unique words:", len(set(text_words)))
print("vocabulary size: ", vocabulary_size)
print("most common words: ", count[:10])

data_index = 0
# generate training batch for the skip-gram model
def next_batch(batch_size, num_skips, sjip_window):
    global data_index
    assert batch_size % num_skips == 0
    assert num_skips <= 2 * skip_window
    batch = np.ndarray(shape=(batch_size), dtype=np.int32)
    labels = np.ndarray(shape=(batch_size, 1) , dtype=np.int32)
    # get window size (words left and right + current one)
    span = 2 * skip_window + 1
    buffer = collections.deque(maxlen=span)
    if data_index + span > len(data):
        data_index = 0
    buffer.extend(data[data_index:data_index + span])
    data_index += span
    for i in range(batch_size // num_skips):  # // 整除
        context_words = [w for w in range(span) if w != skip_window]
        words_to_use = random.sample(context_words, num_skips)
        for j, context_words in enumerate(words_to_use):
            batch[i * num_skips + j] = buffer[skip_window]
            labels[i * num_skips + j, 0] = buffer[context_words]
        if data_index == len(data):
            buffer.extend(data[0:span])
            data_index = span
        else:
            buffer.append(data[data_index])
            data_index += 1
    # backtrack a little bit to avoid skipping words in the end of a batch
    data_index = (data_index + len(data) - span) % len(data)
    return batch, labels

# input data
X = tf.placeholder(tf.int32, shape=[None])
# input label
Y = tf.placeholder(tf.int32, shape=[None, 1])

# ensure the following ops & var are assigned on CPU
# (some ops are not compatible on GPU)
with tf.device('/cpu:0'):
    # creating the embedding variable (each row represent a word embedding vector)
    embedding = tf.Variable(tf.random_normal([vocabulary_size, embedding_size]))
    # lookup the corresponding embedding vectors for each sample in X
    X_embed = tf.nn.embedding_lookup(embedding, X)

    # construct the variables for the NCE loss
    nce_weights = tf.Variable(tf.random_normal([vocabulary_size, embedding_size]))
    nce_biases = tf.Variable(tf.zeros([vocabulary_size, embedding_size]))

# computer the average NCE loss for the batch
loss_op = tf.reduce_mean(
    tf.nn.nce_loss(
        weights=nce_weights,
        biases=nce_biases,
        labels=Y,
        inputs=X_embed,
        num_sampled=num_sampled,
        num_classes=vocabulary_size
    )
)

# define the optimizer
optimizer = tf.train.GradientDescentOptimizer(learning_rate)
train_op = optimizer.minimize(loss_op)

# evaluation
# compute the cosine similarity between input data embedding and every embedding vectors
X_embed_norm = X_embed / tf.sqrt(tf.reduce_sum(tf.square(X_embed)))
embedding_norm = embedding / tf.sqrt(tf.reduce_sum(tf.square(embedding), 1,keepdims=True))
cosine_sim_op = tf.matmul(X_embed_norm, embedding_norm, transpose_b = True)

# initialize the variables
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)

    # testing data
    x_test = np.array([word2id[w]] for w in eval_words)

    average_loss = 0
    for step in range(1, num_steps + 1):
        # get a new batch of data
        batch_x, batch_y = next_batch(batch_size, num_skips, skip_window)
        # run tarining op
        _, loss = sess.run([train_op, loss_op], feed_dict={X: batch_x, Y: batch_y})
        average_loss += loss

        if step % display_steps == 0 or step == 1:
            if step > 1:
                average_loss /= display_steps
            print("step " + str(step) + ", average loss = " + "{:.4f}".format(average_loss))
            average_loss = 0

        # evaluation
        if step % eval_step == 0 or step == 1:
            print("evaluation...")
            sim = sess.run(cosine_sim_op, feed_dict={X: x_test})
            for i in range(len(eval_words)):
                top_k = 8  # number of nearest neighbors
                nearest = (-sim[i, :]).argsort()[1:top_k + 1]
                log_str = '"%s" nearest neightbors: ' % eval_words[i]
                for k in range(top_k):
                    log_str = '%s %s,' %(log_str, id2word[nearest[k]])

                print(log_str)
