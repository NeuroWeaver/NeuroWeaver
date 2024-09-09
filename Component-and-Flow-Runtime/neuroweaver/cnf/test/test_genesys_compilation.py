# Component definition
import ohai.deep_learning as dnn

with Component(outputs=[model_out]) as modelgen:
    model_out = 'custom_conv_layer2.onnx'

onnx_model = modelgen()
dnn.compile_model(onnx_model)
