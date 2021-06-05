from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)
"""
@app.route("/", methods=["GET","POST"])
def add():
   #redirect('/todo')
    if request.method == 'POST':
        # Fetch form data
        title = request.form.get("title")
        complete = False
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Todo(title, complete) VALUES(%s, %s)",(title, complete))
        mysql.connection.commit()
        cur.close()    
        return redirect('/todo')
    return render_template('base.html')

    #new_todo = Todo(title=title, complete=False)
    #db.session.add(new_todo)
    #db.session.commit()
    #return redirect(url_for("home"))
"""
@app.route("/", methods=["GET","POST"])
def home():
    #todo_list = Todo.query.all()
    cur = mysql.connection.cursor()
    resultCom = cur.execute("SELECT * FROM Todo WHERE complete=1")
    resultValue = cur.execute("SELECT * FROM Todo")
    resultUnCom = (resultValue-resultCom)
    if resultValue > 0:
        todo_list = cur.fetchall()
        if request.method == 'POST':
            # Fetch form data
            title = request.form.get("title")
            complete = 0
            #cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Todo(title, complete) VALUES(%s, %s)",(title, complete))
            mysql.connection.commit()
            cur.close()
            return redirect('/')
        return render_template("hello.html", todo_list=todo_list,resultValue=resultValue,resultCom=resultCom,resultUnCom=resultUnCom)
    
    else:
        if request.method == 'POST':
            # Fetch form data
            title = request.form.get("title")
            complete = 0
            #cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Todo(title, complete) VALUES(%s, %s)",(title, complete))
            mysql.connection.commit()	
            cur.close()
            return redirect('/')
        return render_template('hello.html')


@app.route("/update/<int:todo_id>", methods=["POST","GET"])
def update(todo_id):
    #todo = Todo.query.filter_by(id=todo_id).first()
    cur = mysql.connection.cursor()
    complete = cur.execute("SELECT complete FROM Todo WHERE id='%s'",[todo_id])	
    cur.execute("UPDATE Todo SET complete='%s' WHERE id='%s'",(complete,todo_id))
    mysql.connection.commit()
    cur.close()    
    #db.session.commit()
    return redirect(url_for("home"))

@app.route("/incomplete/<int:todo_id>", methods=["POST","GET"])
def incomplete(todo_id):
    #todo = Todo.query.filter_by(id=todo_id).first()
    cur = mysql.connection.cursor()
    complete = cur.execute("SELECT complete FROM Todo WHERE id='%s'",[todo_id])
    complete=0
    cur.execute("UPDATE Todo SET complete='%s' WHERE id='%s'",(complete,todo_id))
    mysql.connection.commit()
    cur.close()    
    #db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>", methods=["POST","GET"])
def delete(todo_id):
    #todo = Todo.query.filter_by(id=todo_id).first()
    #db.session.delete(todo)
    #db.session.commit()  
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Todo WHERE id='%s'",[todo_id])
    mysql.connection.commit()
    cur.close()    
    return redirect(url_for("home"))

if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)
