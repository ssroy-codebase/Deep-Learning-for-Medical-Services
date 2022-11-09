from flask import Flask, render_template
from werkzeug.utils import secure_filename
from flask import Flask, redirect, url_for, request, render_template
import os, json
from image_classification import make_prediction

app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        test_type = request.form['test_type']
        test_type = test_type.split(':')[-1].replace(" ", "")
        
        return redirect(url_for('result', test_type= test_type))

    return render_template('index.html')

@app.route("/result/<string:test_type>",methods=['GET'])
def result(test_type):

    return render_template('result.html')

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method== 'GET':
        return redirect(url_for('result'))
    if request.method == 'POST':
        type = request.form['type']
        # print(type)
        f = request.files['file']
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        result = make_prediction(type, file_path)
        os.remove(file_path)
        return result
    return None

app.run(debug=True)
