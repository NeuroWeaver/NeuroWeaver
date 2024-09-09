import tensorflow as tf


def bias_add(tin, weights):
    inp = tf.placeholder(tf.float32)
    bias = tf.nn.bias_add(inp, weights)
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        out_tensors = sess.run(bias, feed_dict={inp: tin})
    return out_tensors
