from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/flask'
db = SQLAlchemy(app)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    files = db.relationship("File", backref="category", lazy='dynamic')


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    create_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    content = db.Column(db.Text)


@app.route('/')
def index():
    data = db.session.query(File).all()
    return render_template('index.html', data=data)


@app.route('/files/<file_id>')
def file(file_id):
    data = db.session.query(File).filter_by(id=int(file_id)).first_or_404()
    '''
    data = db.session.query(File).filter(File.id==int(file_id)).first()
    if data == None:
        return render_template('404.html'), 404
    '''
    return render_template('file.html', data=data)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
