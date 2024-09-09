import tensorflow as tf


def batch_normalization(tin, mean, variance, gamma):
    inp = tf.placeholder(tf.float32)
    bn0 = tf.nn.batch_normalization(inp, mean, variance, None, gamma, 1e-5)
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        out_tensors = sess.run(bn0, feed_dict={inp: tin})
    return out_tensors
