from flask import Flask, render_template
from werkzeug.utils import secure_filename
from flask import Flask, redirect, url_for, request, render_template
import os
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
    return render_template('result.html',test_type= test_type)

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
            basepath, 'static/images', secure_filename(f.filename))
        f.save(file_path)

        result = make_prediction(type, file_path)
        os.remove(file_path)
        if result[1] == "medical":
            # print(result)
            return result
        else:
            result = result[0] + ". Sample is unknown to the model. So prediction can be false."
            # print(result)
            return result
    return None

if __name__ == "__main__":
    app.run(debug=False)
