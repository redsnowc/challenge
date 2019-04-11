from flask import Flask
from flask import render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.update(
        SECRET_KEY = 'sdfjksfdsfjklsdjflk',
        SQLALCHEMY_DATABASE_URI='mysql+mysqldb://root@localhost:3306/simpledu?charset=utf8'
        )

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
            db.String(32), unique=True, index=True, nullable=False)
    publish_courses = db.relationship('Course')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
            db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
            db.String(128), unique=True, index=True, nullable=False)
    author_id = db.Column(
            db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    author = db.relationship('User', uselist=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
            db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@app.route('/')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@app.route('/admin')
def admin_index():
    return 'admin'

