from PIL import Image, ImageFilter
import requests
from io import BytesIO
import base64


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


def blur_filter(img):
    return img.filter(ImageFilter.GaussianBlur(8))


def edge_filter(img):
    return img.filter(ImageFilter.Kernel(
        size=(3, 3),
        kernel=(-1, -1, -1,
                -1,  8, -1,
                -1, -1, -1),
        scale=1/9,
        offset=0
    ))


def to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('ascii')


# Return results for the webpage
def render_filters(img):
    results_array = [
        {
            "image": to_base64(blur_filter(img)),
            "filter": "GaussianBlur(8)"
        },
        {
            "image": to_base64(edge_filter(img)),
            "filter": "Laplacian"
        }
    ]

    return results_array

