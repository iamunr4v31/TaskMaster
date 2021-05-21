# flask and related imports
from flask import Flask, request, render_template, redirect, url_for
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

# to parse date
from datetime import datetime

# icecream is used to debug
from icecream import ic

# to establish path connection to database
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.realpath(__file__)), r'database\taskmaster.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)
    deadline = db.Column(db.DateTime, nullable=True, default=None)

@app.route("/")
def index():
    incompleteTasks = Task.query.filter_by(complete=False).all()
    completeTasks = Task.query.filter_by(complete=True).all()
    # ic(incompleteTasks)
    # ic(completeTasks)
    return render_template('index.html', incomplete=incompleteTasks, complete=completeTasks)

@app.route("/add", methods=['POST'])
def add():
    ipTask = request.form['taskInput']
    dateTime = request.form['taskDeadLine']
    if dateTime != '':
        dateTime = datetime.fromisoformat(request.form['taskDeadLine'])
    else:
        dateTime = None
    task = Task(text=ipTask, deadline=dateTime, complete=False)
    # ic(task.__dict__)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    checkList = request.form.getlist('updateCheck')
    # ic(checkList)
    for checkId in checkList:
        Task.query.filter_by(id=checkId).first().complete = True
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)