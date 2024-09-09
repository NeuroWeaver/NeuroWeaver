import tensorflow as tf


def max_pool(t_in, ksize, strides, padding):
    inp = tf.placeholder(tf.float32)
    t_out = tf.nn.max_pool(inp, ksize=ksize, strides=strides, padding=padding)
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        out_tensors = sess.run(t_out, feed_dict={inp: t_in})
    return out_tensors
