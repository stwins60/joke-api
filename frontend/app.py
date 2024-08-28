from flask import Flask, render_template, url_for, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/style.css')
def style():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'style.css')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)