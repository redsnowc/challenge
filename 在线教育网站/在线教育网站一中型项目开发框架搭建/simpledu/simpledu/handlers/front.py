from flask import Blueprint
from flask import render_template
from simpledu.models import Course

front = Blueprint('front', __name__)

@front.route('/')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)
