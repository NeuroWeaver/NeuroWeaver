import tensorflow as tf


def conv2d(tin, weights, strides, padding):
    inp = tf.placeholder(tf.float32)
    conv0 = tf.nn.conv2d(inp, weights, strides=strides, padding=padding)
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        out_tensors = sess.run(conv0, feed_dict={inp: tin})
    return out_tensors
