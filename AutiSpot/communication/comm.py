from flask import Flask, render_template, request, redirect, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os, sys
from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
import yaml
from extensions import mysql


communication = Blueprint("communication", __name__ , static_folder = "communication/static", template_folder = "templates")

"""
class Config(object):
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = ''
    MYSQL_DATABASE_DB = 'shabby95'
    MYSQL_DATABASE_HOST = 'localhost'
"""
app = Flask(__name__)
#app.config.from_object(Config)
# Configure db

#db = yaml.load(open('db1.yaml'))
"""
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'shabby95'

mysql.init_app(app)
"""


UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#Main ROute Path
@communication.route('/admin_pan', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        style = userDetails['style']

        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Can also rename the uploaded file if you want
            #os.rename(UPLOAD_FOLDER + filename, UPLOAD_FOLDER+'niloofar.jpg')
            FILEPATH = UPLOAD_FOLDER + filename
            

            # Create db connection to upload new file
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (name1, name, filepath, style) VALUES (%s,%s,%s,%s)", (name, filename, FILEPATH,style))
            mysql.connection.commit()
            
            print ("\nSuccessfully added a file to the database (specified uploading folder).")
            print (" Name: " + filename)
            print (" Path: " + FILEPATH)
         
        file_audio = request.files['file_audio']
        if file_audio and allowed_file(file_audio.filename):
            filename = secure_filename(file_audio.filename)
            file_audio.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Can also rename the uploaded file if you want
            #os.rename(UPLOAD_FOLDER + filename, UPLOAD_FOLDER+'niloofar.jpg')
            AUDIOPATH = UPLOAD_FOLDER + filename
            

            # Create db connection to upload new file
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET audio = %s ,audiopath = %s WHERE name1 = %s" , (filename, AUDIOPATH, name))
            mysql.connection.commit()
            cur.close()
            print ("\nSuccessfully added a file to the database (specified uploading folder).")
            print (" Name: " + filename)
            print (" Path: " + AUDIOPATH)
        return redirect('/users')
    return render_template('panel.html')





#Positive Comments
@communication.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users WHERE style='Chat' OR style='Things' OR style='Activities' OR style='People' OR style='Relations' OR style='Places'")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('now-ui-dashboard-master/examples/dashboard.html',userDetails=userDetails)


"""

#Negative Comments
@communication.route('/negative')
def negative():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users WHERE style='Negative' ORDER BY id ASC ")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('now-ui-dashboard-master/examples/icons.html',userDetails=userDetails)


#noun
@communication.route('/noun')
def noun():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users WHERE style='Noun/Object' ORDER BY id ASC ")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('now-ui-dashboard-master/examples/map.html',userDetails=userDetails)


#Complimentary Comments
@communication.route('/compliments')
def compliments():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users WHERE style='Compliment' ORDER BY id ASC ")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('now-ui-dashboard-master/examples/notifications.html',userDetails=userDetails)





if __name__ == '__main__':
    app.run(debug=True)

"""








