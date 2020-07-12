"""
Tutorial borrowed from
https://pytorch.org/tutorials/recipes/deployment_with_flask.html

Last edited by Kamal Gupta <kamalgupta308@gmail.com>
"""
import traceback
from flask import Flask, jsonify, request, render_template

from utils import read_file, transform_image, get_topk, render_prediction

app = Flask(__name__)


@app.route('/', methods=['GET'])
def demo_photag():
    return render_template('photag.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        try:
            url = request.args.get('q')
            app.logger.debug('url provided - %s', url)
            input_tensor = transform_image(read_file(url=url))
            values, indices = get_topk(input_tensor)
            results = render_prediction(values, indices)
            return jsonify(results=results)

        except:
            app.logger.debug("Error: %s", traceback.print_exc())
            return jsonify("invalid image url")

    elif request.method == 'POST':
        try:
            file = request.files['file']
            app.logger.debug('file uploaded - %s', file)
            url = request.form.get("url", None)
            app.logger.debug('url provided - %s', url)

            input_tensor = transform_image(read_file(upload=file, url=url))
            values, indices = get_topk(input_tensor)
            results = render_prediction(values, indices)
            return jsonify(results=results)

        except:
            app.logger.debug("Error: %s", traceback.print_exc())
            return jsonify("invalid image")

    else:
        app.logger.debug("Error: %s", traceback.print_exc())
        return jsonify('invalid request')


if __name__ == '__main__':
    app.run()
