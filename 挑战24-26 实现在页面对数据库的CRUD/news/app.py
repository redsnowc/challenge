from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pymongo import MongoClient
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key='dfjdsfkjlas'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/flask'
db = SQLAlchemy(app)

class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    name = StringField('Category', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditForm(ArticleForm):
    submit = SubmitField('Update')

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')

class AddTag(FlaskForm):
    tag = StringField('Tag Name', validators=[DataRequired()])
    submit = SubmitField('Add')

class DeleteTag(FlaskForm):
    submit = SubmitField('-')

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    files = db.relationship("File", backref='category')


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    create_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    content = db.Column(db.Text)
    
    @staticmethod
    def add_tag(file, tag_name):
        client = MongoClient('127.0.0.1', 27017)
        mg_db = client.tag
        if mg_db.tag.find_one({'id': file.id}) == None:
            mg_db.tag.insert({'id': file.id, 'tag': [tag_name]})
        else:
            mg_db.tag.update({'id': file.id}, {'$push': {'tag': tag_name}})


@app.route('/')
def index():
    form1 = DeleteForm()
    form2 = DeleteTag()
    data = db.session.query(File).all()
    client = MongoClient('127.0.0.1', 27017)
    mg_db = client.tag
    return render_template(
            'index.html', data=data, mg_db=mg_db, form1=form1, form2=form2)

@app.route('/files/<int:file_id>')
def file(file_id):
    data = File.query.filter_by(id=file_id).first_or_404()
    return render_template('file.html', data=data)

@app.route('/new', methods=['GET', 'POST'])
def new():
    form = ArticleForm()
    if form.validate_on_submit():
        name = form.name.data
        content = form.content.data
        title = form.title.data
        create_time = datetime.utcnow()
        if Category.query.filter_by(name=name).first():
            category = Category.query.filter_by(name=name).first()
        else:
            category = Category(name=name)
        file = File(
                title=title, 
                create_time=create_time,  
                content=content)
        db.session.add(category)
        db.session.add(file)
        category.files.append(file)
        db.session.commit()
        return redirect(url_for('file', file_id=file.id))
    return render_template('new.html', form=form)

@app.route('/edit/<int:file_id>', methods=['GET','POST'])
def edit(file_id):
    form = EditForm()
    file = File.query.get(file_id)
    category = file.category
    if form.validate_on_submit():
        name = form.name.data
        file.title = form.title.data
        file.content = form.content.data
        file.name = name
        if Category.query.filter_by(name=name).first():
            category = Category.query.filter_by(name=name).first()
        else:
            category = Category(name=name)
        category.files.append(file)
        db.session.commit()
        return redirect(url_for('file', file_id=file.id))
    form.name.data = category.name
    form.title.data = file.title
    form.content.data = file.content
    return render_template('edit_form.html', form=form)

@app.route('/delete/<int:file_id>', methods=['POST'])
def delete(file_id):
    form = DeleteForm()
    if form.validate_on_submit():
        file = File.query.get(file_id)
        db.session.delete(file)
        db.session.commit()
        client = MongoClient('127.0.0.1', 27017)
        mg_db = client.tag
        mg_db.tag.delete_one({"id": file_id })
    else:
        return render_template('404.html'), 404
    return redirect(url_for('index'))

@app.route('/addtag/<int:file_id>', methods=['GET', 'POST'])
def addtag(file_id):
    form = AddTag()
    file = File.query.get(file_id)
    if form.validate_on_submit():
        tag = form.tag.data
        File.add_tag(file, tag)
        return redirect(url_for('index'))
    return render_template('tag.html', form=form)    

@app.route('/deletetag/<int:file_id><tagname>', methods=['POST'])
def deletetag(tagname, file_id):
    form = DeleteTag()
    if form.validate_on_submit():
        client = MongoClient('127.0.0.1', 27017)
        mg_db = client.tag
        mg_db.tag.update_many({"id": file_id}, {"$pull": {"tag": tagname}})
    else:
        return render_template('404.html'), 404
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
