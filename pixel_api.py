from flask import Flask, render_template, request, redirect, url_for
import os 
from werkzeug.utils import secure_filename
import cv2
import base64
import numpy as np

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = 'SECRETKEY'

def img_converter(img_data, col, siz):
    nparr = np.fromstring(img_data, np.uint8)
    if col == "Colored":
        if siz == 'Original':
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        elif siz == '1/2':
            img = cv2.imdecode(nparr, cv2.IMREAD_REDUCED_COLOR_2)
        elif siz == '1/4':
            img = cv2.imdecode(nparr, cv2.IMREAD_REDUCED_COLOR_4) 
    elif col == "Gray_Scale":
        if siz == 'Original':
            img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        elif siz == '1/2':
            img = cv2.imdecode(nparr, cv2.IMREAD_REDUCED_GRAYSCALE_2)
        elif siz == '1/4':
            img = cv2.imdecode(nparr, cv2.IMREAD_REDUCED_GRAYSCALE_4)
        
    retval, buffer = cv2.imencode('.jpg', img)
    grey_base64 = base64.b64encode(buffer).decode('utf-8')
    return grey_base64

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/home", methods=['GET', 'POST'])
def upload_image():
    image = request.files['image'].read()
    size = request.form.get('size_')
    color = request.form.get('color_')
    brigh = request.form.get('brightness')

    output_img = img_converter(image,color,size)

    return render_template('index.html', return_file=output_img) #return_file=output_img) 


if __name__ == "__main__":
    app.run(debug=True)