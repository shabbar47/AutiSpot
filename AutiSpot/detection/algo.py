
from __future__ import division, print_function
from flask import Flask, render_template, request, Blueprint
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler


# Flask application for uploading photos and testing prediction using .h5 model!

# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer
#---------------------------------------------------------------


detection = Blueprint('detection', __name__, static_folder = "detection/static", template_folder = "templates")

app = Flask(__name__)
model1 = pickle.load(open('model/logistic_regression_model.pkl', 'rb'))
model2 = pickle.load(open('model/decision_tree_model.pkl', 'rb'))
model3 = pickle.load(open('model/KNN_model.pkl', 'rb'))

# Model saved with Keras model.save()
MODEL_PATH ='model/model_vgg19.h5'

# Load your trained model
model = load_model(MODEL_PATH)






@detection.route('/detection',methods=['GET'])
def Home():
    return render_template('detect.html')


standard_to = StandardScaler()
@detection.route("/predict_ml", methods=['POST'])
def predict_ml():
    if request.method == 'POST':
        A1=request.form['A1']
        if(A1=='always' or A1=='usually'):
                A1=0
        else:
            A1=1
        A2=request.form['A2']
        if(A2=='always' or A2=='usually'):
                A2=0
        else:
            A2=1
        A3=request.form['A3']
        if(A3=='always' or A3=='usually'):
                A3=0
        else:
            A3=1
        A4=request.form['A4']
        if(A4=='always' or A4=='usually'):
                A4=0
        else:
            A4=1
            
        A5=request.form['A5']
        if(A5=='always' or A5=='usually'):
            A5=0
        else:
            A5=1	
        A6=request.form['A6']
        if(A6=='always' or A6=='usually'):
            A6=0
        else:
            A6=1
        A7=request.form['A7']
        if(A7=='always' or A7=='usually'):
            A7=0
        else:
            A7=1
        A8=request.form['A8']
        if(A8=='always' or A8=='usually'):
            A8=0
        else:
            A8=1
        A9=request.form['A9']
        if(A9=='always' or A9=='usually'):
            A9=0
        else:
            A9=1
        A10=request.form['A10']
        if(A10=='always' or A10=='usually'):
            A10=0
        else:
            A10=1
        
        Age=int(request.form['Age'])
         
        sex=request.form['sex']
        if(sex=='male'):
            sex=1
        else:
            sex=0
            
        ethnicity=request.form['ethnicity']
        if(ethnicity=='middle eastern'):
            ethnicity=8
        elif(ethnicity=='white european'):
            ethnicity=5
        elif(ethnicity=='hispanic'):
            ethnicity=0
        elif(ethnicity=='black'):
            ethnicity=7
        elif(ethnicity=='asian'):
            ethnicity=6
        elif(ethnicity=='south asian'):
            ethnicity=10
        elif(ethnicity=='native indian'):
            ethnicity=2
        elif(ethnicity=='latino'):
            ethnicity=1
        elif(ethnicity=='mixed'):
            ethnicity=9
        elif(ethnicity=='pacifica'):
            ethnicity=4
        else:
            ethnicity=3
    
        jaundice=request.form['jaundice']
        if(jaundice=='Yes'):
            jaundice=1
        else:
            jaundice=0
            
        family=request.form['family']
        if(family=='Yes'):
            family=1
        else:
            family=0
            
        prediction=model1.predict([[A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,Age,sex,ethnicity,jaundice,family]])
        output=prediction
        print(output)
        if output == 0:
            x='No Autism - As diagnosed by Logistic Regression Algorithm'
        elif output == 1:
            x="Autism - As diagnosed by Logistic Regression Algorithm"
        else:
            x="Error"
    
        prediction2=model2.predict([[A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,Age,sex,ethnicity,jaundice,family]])
        output2=prediction2
        print(output2)
        if output2 == 0:
            y="No Autism - On prognosis by Decision Tree Algorithm"
        elif output2 == 1:
            y="Autism - On prognosis by Decision Tree Algorithm"
        else:
            y="Error"
    

        prediction3=model3.predict([[A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,Age,sex,ethnicity,jaundice,family]])
        output3=prediction3
        print(output3)
        if output3 == 0:
            z="No Autism - As detected by k-Nearest Neighbour Algorithm"
        elif output3 == 1:
            z="Autism - As detected by k-Nearest Neighbour Algorithm"
        else:
            z="Error"
        return render_template('detect.html',a=x,b=y,c=z)    
    
    
    else:
        return render_template('detect.html')



def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)
   


    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    if preds==0:
        preds="AUTISTIC"
    else:
        preds="NON-AUTISTIC"
    
    
    return preds


@detection.route('/CNN', methods=['GET'])
def index():
    # Main page
    return render_template('detect.html')


@detection.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result=preds
        return result
    return None






#if __name__=="__main__":
 #   app.run(debug=True)

