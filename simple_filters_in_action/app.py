"""
Tutorial borrowed from
https://pytorch.org/tutorials/recipes/deployment_with_flask.html

Last edited by Kamal Gupta <kamalgupta308@gmail.com>
"""
import traceback
from flask import Flask, jsonify, request, render_template

from utils import read_file, render_filters


app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@app.route('/button', methods=['GET', 'POST'])
def button():
    if request.method == 'GET':
        try:
            url = request.args.get('q')
            app.logger.debug('url provided - %s', url)
            pil_img = read_file(url=url)
            results = render_filters(pil_img)
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

            pil_img = read_file(upload=file, url=url)
            results = render_filters(pil_img)
            return jsonify(results=results)

        except:
            app.logger.debug("Error: %s", traceback.print_exc())
            return jsonify("invalid image")

    else:
        app.logger.debug("Error: %s", traceback.print_exc())
        return jsonify('invalid request')


if __name__ == '__main__':
    app.run()
