'''
Honor:https://stackoverflow.com/questions/38164798/does-tensorflow-have-cross-validation-implemented-for-its-users
'''

from sklearn.model_selection import KFold
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# Parameters
learning_rate = 0.01
batch_size = 500

# TF graph
x = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, [None, 10])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
pred = tf.nn.softmax(tf.matmul(x, W) + b)
cost = tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred), reduction_indices=1))
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
init = tf.global_variables_initializer()

mnist = input_data.read_data_sets("data/mnist-tf", one_hot=True)
train_x_all = mnist.train.images
train_y_all = mnist.train.labels
test_x = mnist.test.images
test_y = mnist.test.labels

def run_train(session, train_x, train_y):
  print "\nStart training"
  session.run(init)
  for epoch in range(10):
    total_batch = int(train_x.shape[0] / batch_size)
    for i in range(total_batch):
      batch_x = train_x[i*batch_size:(i+1)*batch_size]
      batch_y = train_y[i*batch_size:(i+1)*batch_size]
      _, c = session.run([optimizer, cost], feed_dict={x: batch_x, y: batch_y})
      if i % 50 == 0:
        print "Epoch #%d step=%d cost=%f" % (epoch, i, c)

def cross_validate(session, split_size=5):
  results = []
  kf = KFold(n_splits=split_size)
  for train_idx, val_idx in kf.split(train_x_all, train_y_all):
    train_x = train_x_all[train_idx]
    train_y = train_y_all[train_idx]
    val_x = train_x_all[val_idx]
    val_y = train_y_all[val_idx]
    run_train(session, train_x, train_y)
    results.append(session.run(accuracy, feed_dict={x: val_x, y: val_y}))
  return results

with tf.Session() as session:
  result = cross_validate(session)
  print "Cross-validation result: %s" % result
  print "Test accuracy: %f" % session.run(accuracy, feed_dict={x: test_x, y: test_y})
