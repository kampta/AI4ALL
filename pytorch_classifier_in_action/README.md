Building a photo tagging app with PyTorch
=========================================

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kampta/AI4ALL/blob/master/pytorch_classifier_in_action/pytorch_flask_tutorial.ipynb)

A simple flask web app with REST API and a pre-trained PyTorch model

![pytorch_in_action](imgs/classification.gif)

* [PyTorch](https://pytorch.org/) is a machine learning framework for research and development of ML models.
* [Flask](http://flask.pocoo.org/) is a micro web framework powered by Python.

## Prerequisites

The code has been tested with
* Flask==1.1
* requests==2.24
* Pillow==7.1
* torch==1.4
* torchvision=0.5

Install everything with `pip install -r requirements.txt`

## Getting started

(optional)
```
export FLASK_ENV=development
```

Run
```
FLASK_APP=app.py flask run
```

and open http://localhost:5000 in your browser

## Testing with `curl`

* `GET`
```
curl -X GET -H "Content-Type: application/json" http://localhost:5000/predict?q=https://icatcare.org/app/uploads/2018/07/Thinking-of-getting-a-cat.png
```

* `POST`
```
curl -X POST -H "Content-Type: multipart/form-data" http://localhost:5000/predict -F "file=@dog.jpg"
```

## Credits

This tutorial heavily borrows from

* https://pytorch.org/tutorials/intermediate/flask_rest_api_tutorial.html
* https://www.pyimagesearch.com/2014/12/08/adding-web-interface-image-search-engine-flask