import onnx
import onnxsim
import torch
from torchsummary import summary

pth_path = "../../runs/pretrain/botnet/weights/epoch120.pt"
onnx_path = "../../runs/pretrain/botnet/weights/epoch120.onnx"

model = torch.load(pth_path)["model"].to("cuda")
summary(model, batch_size=1, input_size=(3, 224, 224), device="cuda")
model.eval()

data = torch.rand((1, 3, 224, 224), dtype=torch.float32, device="cuda")
torch.onnx.export(model, data, onnx_path, verbose=False, opset_version=12,
                  input_names=["images"], output_names=["output"],
                  # dynamic_axes={
                  #     'images': {0: 'batch_size'},
                  #     'output': {0: 'batch_size'}}
                  )

# Checks
model_onnx = onnx.load(onnx_path)  # load onnx model
onnx.checker.check_model(model_onnx)  # check onnx model

# Simplify
try:
    print(f'simplifying with onnxsim {onnxsim.__version__}...')
    model_onnx, check = onnxsim.simplify(model_onnx)
    assert check, 'Simplified ONNX model could not be validated'
except Exception as e:
    print(f'simplifier failure: {e}')

onnx.save(model_onnx, onnx_path)
