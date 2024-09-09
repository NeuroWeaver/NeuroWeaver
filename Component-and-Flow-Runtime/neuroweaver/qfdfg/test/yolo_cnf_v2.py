import pickle
import sys
import os
import cv2
import collections
import numpy as np
import copy
import logging
import collections
from time import time
from darkflow.net.build import TFNet

sys.path.append('/Users/joon/dnnweaver2')
sys.path.append('/Users/joon/dnnweaver2/example')
from yolo_tf.yolo2_tiny_tf import YOLO2_TINY_TF
from dnn_fpga import dnn_fpga



with Component(outputs=[input_im, input_png]) as image_fetch:
    input_png = '/Users/joon/ohai.src/axelvm/test.jpg'
    bf_weight_pickle = '/Users/joon/dnnweaver2/example/weights/yolo2_tiny_dnnweaver2_weights.pickle'
    input_im = cv2.imread(input_png, cv2.IMREAD_COLOR)

with Component(inputs=[input_im], outputs=[out_tensors_d, tfnet]) as yolo_dnn:
    weight_pickle = '/Users/joon/dnnweaver2/example/weights/yolo2_tiny_tf_weights.pickle'
    options = {"model": "/Users/joon/dnnweaver2/example/conf/tiny-yolo-voc.cfg", "load": "/Users/joon/dnnweaver2/example/weights/tiny-yolo-voc.weights", "threshold": 0.25}
    tfnet = TFNet(options)
    im = tfnet.framework.resize_input(input_im)
    tin = np.expand_dims(im, 0)
    my_tin = copy.deepcopy(tin)
    fpga_tin = copy.deepcopy(tin)
    y2t_tf = YOLO2_TINY_TF([1, 416, 416, 3], weight_pickle)
    nodes, out_tensors = y2t_tf._inference(my_tin)
    out_tensors_d = collections.OrderedDict()
    cnt = 0
    for i in range(len(nodes)):
        node = nodes[i]
        if "Maximum" in node.name:
            if "Maximum_7" in node.name:
                out_tensors_d["conv7"] = out_tensors[i]
            else:
                out_tensors_d["conv" + str(cnt)] = out_tensors[i]
        if "MaxPool" in node.name:
            out_tensors_d["pool" + str(cnt)] = out_tensors[i]
            cnt += 1
        if "BiasAdd_8" in node.name:
            out_tensors_d["conv8"] = out_tensors[i]

with Component(inputs=[out_tensors, tfnet, input_im], outputs=[boxesInfo]) as bbox_drawer:
    h, w, _ = input_im.shape
    boxes = tfnet.framework.findboxes(out_tensors["conv8"][0])
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

with Component(inputs=[bbox_info, input_im, input_png]) as display:
    font = cv2.FONT_HERSHEY_SIMPLEX
    for det in bbox_info:
        label, l, r, t, b = det['label'], det['topleft']['x'], det['bottomright']['x'], det['topleft']['y'], det['bottomright']['y']
        cv2.rectangle(input_im, (l, b), (r, t), (0, 255, 0), 2)
        if "4.0.0" in cv2.__version__ or "3.4.5" in cv2.__version__:
            cv2.putText(input_im, label, (l, b), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        elif "2.4.9.1" in cv2.__version__:
            cv2.putText(input_im, label, (l, b), font, 1, (255, 255, 255), 2, cv2.CV_AA)
        else:
            raise Exception("Unknown cv2 version")
    cv2.imwrite("bbox-" + os.path.basename(input_png), input_im)


img_ndarray, img_png = image_fetch()
out_tensors, tfnet = yolo_dnn(img_ndarray)
bbox_info = bbox_drawer(out_tensors, tfnet, img_ndarray)
display(bbox_info, img_ndarray, img_png)
