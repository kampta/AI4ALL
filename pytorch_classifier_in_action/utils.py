import os
import json

import torch
import torchvision.transforms as transforms
import torchvision.models as models

from PIL import Image
import requests
from io import BytesIO

img_class_map = None
mapping_file_path = 'index_to_name.json'                  # Human-readable names for Imagenet classes
if os.path.isfile(mapping_file_path):
    with open (mapping_file_path) as f:
        img_class_map = json.load(f)

model = models.resnet50(pretrained=True)                  # Trained on 1000 classes from ImageNet
model.eval()                                              # Turns off autograd and


# Read either file or a url
def read_file(upload=None, url=None):
    if (upload is not None) and upload.filename:
        in_memory_file = BytesIO()
        upload.save(in_memory_file)
        img = Image.open(in_memory_file)
        return img

    elif url is not None:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img

    else:
        raise NameError('Invalid file/url')


# Transform input into the form our model expects
def transform_image(pil_image):
    input_transforms = [
        transforms.Resize(255),           # We use multiple TorchVision transforms to ready the image
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.485, 0.456, 0.406],       # Standard normalization for ImageNet model input
            [0.229, 0.224, 0.225]
        )
    ]
    my_transforms = transforms.Compose(input_transforms)
    timg = my_transforms(pil_image)                       # Transform PIL image to appropriately-shaped PyTorch tensor
    timg.unsqueeze_(0)                                    # PyTorch models expect batched input; create a batch of 1
    return timg


# Get a prediction
def get_topk(input_tensor, k=5):
    outputs = model.forward(input_tensor)                 # Get likelihoods for all ImageNet classes
    values, indices = torch.topk(outputs, k)              # Extract top k most likely classes
    values = values.data.cpu().numpy()[0]
    indices = indices.data.cpu().numpy()[0]
    return values, indices


# Make the prediction human-readable
def render_prediction(values, indices):
    results_array = []

    for value, idx in zip(values, indices):
        results_array.append({
            "label": img_class_map.get(str(idx), "Unknown")[1],
            "score": str(value)
        })

    return results_array

