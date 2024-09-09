import tensorflow as tf


def maximum(tin1, tin2):
    inp1 = tf.placeholder(tf.float32)
    inp2 = tf.placeholder(tf.float32)
    tout = tf.maximum(inp1, inp2)
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        out_tensors = sess.run(tout, feed_dict={inp1: tin1, inp2: tin2})
    return out_tensors
