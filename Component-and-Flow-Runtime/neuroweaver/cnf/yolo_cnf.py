import numpy as np
import cv2
import pickle
import collections
import os
from darkflow.net.build import TFNet

import ohai.deep_learning as dnn


with Component() as main:
    input_jpg = '/Users/joon/neuroweaver/runtime/test.jpg'
    options = {"model": "/Users/joon/dnnweaver2/example/conf/tiny-yolo-voc.cfg", "load": "/Users/joon/dnnweaver2/example/weights/tiny-yolo-voc.weights", "threshold": 0.25}
    tfnet = TFNet(options)
    input_im = cv2.imread(input_jpg)
    im = tfnet.framework.resize_input(input_im)
    tin = np.expand_dims(im, 0)
    weights = '/Users/joon/dnnweaver2/example/weights/yolo2_tiny_tf_weights.pickle'
    with open(weights, "rb") as f:
        weights = pickle.load(f, encoding='latin1')
    with Component(inputs=[tin], outputs=[tout], state=[weights]) as yolo_dnn:
        conv0  =  dnn.conv2d(tin, weights[0]["kernel"], [1, 1, 1, 1], 'SAME')
        bias0  =  dnn.bias_add(conv0, weights[0]["biases"])
        bn0    =  dnn.batch_normalization(bias0, weights[0]["moving_mean"], weights[0]["moving_variance"], weights[0]["gamma"])
        l1     =  dnn.maximum(bn0, 0.1 * bn0)
        p2     =  dnn.max_pool(l1, [1, 2, 2, 1], [1, 2, 2, 1], 'SAME')
        conv3  =  dnn.conv2d(p2, weights[1]["kernel"], [1, 1, 1, 1], 'SAME')
        bias3  =  dnn.bias_add(conv3, weights[1]["biases"])
        bn3    =  dnn.batch_normalization(bias3, weights[1]["moving_mean"], weights[1]["moving_variance"], weights[1]["gamma"])
        l4     =  dnn.maximum(bn3, .1 * bn3)
        p5     =  dnn.max_pool(l4, [1, 2, 2, 1], [1, 2, 2, 1], 'SAME')
        conv6  =  dnn.conv2d(p5, weights[2]["kernel"], [1, 1, 1, 1], 'SAME')
        bias6  =  dnn.bias_add(conv6, weights[2]["biases"])
        bn6    =  dnn.batch_normalization(bias6, weights[2]["moving_mean"], weights[2]["moving_variance"], weights[2]["gamma"])
        l7     =  dnn.maximum(bn6, .1 * bn6)
        p8     =  dnn.max_pool(l7, [1, 2, 2, 1], [1, 2, 2, 1], 'SAME')
        conv9  =  dnn.conv2d(p8, weights[3]["kernel"], [1, 1, 1, 1], 'SAME')
        bias9  =  dnn.bias_add(conv9, weights[3]["biases"])
        bn9    =  dnn.batch_normalization(bias9, weights[3]["moving_mean"], weights[3]["moving_variance"], weights[3]["gamma"])
        l10    =  dnn.maximum(bn9, .1 * bn9)
        p11    =  dnn.max_pool(l10, [1, 2, 2, 1], [1, 2, 2, 1], 'SAME')
        conv12 =  dnn.conv2d(p11, weights[4]["kernel"], [1, 1, 1, 1], 'SAME')
        bias12 =  dnn.bias_add(conv12, weights[4]["biases"])
        bn12   =  dnn.batch_normalization(bias12, weights[4]["moving_mean"], weights[4]["moving_variance"], weights[4]["gamma"])
        l13    =  dnn.maximum(bn12, .1 * bn12)
        p14    =  dnn.max_pool(l13, [1, 2, 2, 1], [1, 2, 2, 1], 'SAME')
        conv15 =  dnn.conv2d(p14, weights[5]["kernel"], [1, 1, 1, 1], 'SAME')
        bias15 =  dnn.bias_add(conv15, weights[5]["biases"])
        bn15   =  dnn.batch_normalization(bias15, weights[5]["moving_mean"], weights[5]["moving_variance"], weights[5]["gamma"])
        l16    =  dnn.maximum(bn15, .1 * bn15)
        p17    =  dnn.max_pool(l16, [1, 2, 2, 1], [1, 1, 1, 1], 'SAME')
        conv18 =  dnn.conv2d(p17, weights[6]["kernel"], [1, 1, 1, 1], 'SAME')
        bias18 =  dnn.bias_add(conv18, weights[6]["biases"])
        bn18   =  dnn.batch_normalization(bias18, weights[6]["moving_mean"], weights[6]["moving_variance"], weights[6]["gamma"])
        l19    =  dnn.maximum(bn18, .1 * bn18)
        conv20 =  dnn.conv2d(l19, weights[7]["kernel"], [1, 1, 1, 1], 'SAME')
        bias20 =  dnn.bias_add(conv20, weights[7]["biases"])
        bn20   =  dnn.batch_normalization(bias20, weights[7]["moving_mean"], weights[7]["moving_variance"], weights[7]["gamma"])
        l21    =  dnn.maximum(bn20, .1 * bn20)
        conv22 =  dnn.conv2d(l21, weights[8]["kernel"], [1, 1, 1, 1], 'SAME')
        tout   =  dnn.bias_add(conv22, weights[8]["biases"])
    out_tensor =  yolo_dnn(tin, weights)
    with Component(inputs=[tfnet, box_input, h, w], outputs=[boxesInfo]) as bbox_drawer:
        boxes = tfnet.framework.findboxes(box_input)
        threshold = tfnet.FLAGS.threshold
        boxesInfo = list()
        for box in boxes:
            tmpBox = tfnet.framework.process_box(box, h, w, threshold)
            if tmpBox is None:
                continue
            boxesInfo.append({
                "label": tmpBox[4],
                "confidence": tmpBox[6],
                "topleft": {
                    "x": tmpBox[0],
                    "y": tmpBox[2]},
                "bottomright": {
                    "x": tmpBox[1],
                    "y": tmpBox[3]}
            })
    h, w, _ = input_im.shape
    result = bbox_drawer(tfnet, out_tensor[0], h, w)
    with Component(inputs=[result, input_im, input_jpg]) as display:
        font = cv2.FONT_HERSHEY_SIMPLEX
        for det in result:
            label, l, r, t, b = det['label'], det['topleft']['x'], det['bottomright']['x'], det['topleft']['y'], det['bottomright']['y']
            cv2.rectangle(input_im, (l, b), (r, t), (0, 255, 0), 2)
            if "4.0.0" in cv2.__version__ or "3.4.5" in cv2.__version__:
                cv2.putText(input_im, label, (l, b), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            elif "2.4.9.1" in cv2.__version__:
                cv2.putText(input_im, label, (l, b), font, 1, (255, 255, 255), 2, cv2.CV_AA)
            else:
                raise Exception("Unknown cv2 version")
        cv2.imwrite("bbox-" + os.path.basename(input_jpg), input_im)
    display(result, input_im, input_jpg)


main()
