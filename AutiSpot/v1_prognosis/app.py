from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('logistic_regression_model.pkl', 'rb'))
model2 = pickle.load(open('decision_tree_model.pkl', 'rb'))
model3 = pickle.load(open('KNN_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        A1=request.form['A1']
        if(A1=='Yes'):
                A1=1
        else:
            A1=0
        A2=request.form['A2']
        if(A2=='Yes'):
                A2=1
        else:
            A2=0
        A3=request.form['A3']
        if(A3=='Yes'):
                A3=1
        else:
            A3=0
        A4=request.form['A4']
        if(A4=='Yes'):
                A4=1
        else:
            A4=0
            
        A5=request.form['A5']
        if(A5=='Yes'):
            A5=1
        else:
            A5=0	
        A6=request.form['A6']
        if(A6=='Yes'):
            A6=1
        else:
            A6=0
        A7=request.form['A7']
        if(A7=='Yes'):
            A7=1
        else:
            A7=0
        A8=request.form['A8']
        if(A8=='Yes'):
            A8=1
        else:
            A8=0
        A9=request.form['A9']
        if(A9=='Yes'):
            A9=1
        else:
            A9=0
        A10=request.form['A10']
        if(A10=='Yes'):
            A10=1
        else:
            A10=0
        
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
            
        prediction=model.predict([[A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,Age,sex,ethnicity,jaundice,family]])
        output=prediction
        print(output)
        if output == 0:
            x="No autism (Logistic Regression)"
        elif output == 1:
            x="Autism (Logistic Regression)"
        else:
            x="Error"
    
        prediction2=model2.predict([[A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,Age,sex,ethnicity,jaundice,family]])
        output2=prediction2
        print(output2)
        if output2 == 0:
            y="No autism (Decision tree)"
        elif output2 == 1:
            y="Autism (Decision tree)"
        else:
            y="Error"
    

        prediction3=model3.predict([[A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,Age,sex,ethnicity,jaundice,family]])
        output3=prediction3
        print(output3)
        if output3 == 0:
            z="No autism (KNN)"
        elif output3 == 1:
            z="Autism (KNN)"
        else:
            z="Error"
        return render_template('index.html',prediction_text=x,a=y,b=z)    
    
    
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

