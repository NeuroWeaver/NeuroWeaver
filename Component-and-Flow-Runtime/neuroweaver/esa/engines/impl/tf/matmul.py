import tensorflow as tf


def matmul(t_in1, t_in2):
    inp1 = tf.placeholder(tf.float32)
    inp2 = tf.placeholder(tf.float32)
    t_out = tf.matmul(inp1, inp2)
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        out_tensors = sess.run(t_out, feed_dict={inp1: t_in1, inp2: t_in2})
    return out_tensors
