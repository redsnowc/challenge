from flask import Blueprint, render_template
from simpledu.models import Live

live = Blueprint('live', __name__, url_prefix='/live')

@live.route('/')
def index():
    lives = Live.query.all()
    url_live = Live.query.first().live_url
    return render_template('live/index.html', lives=lives, url_live=url_live)

@live.route('/haha')
def haha():
    return 'haha'

@live.route('/xixi/')
def xixi():
    return 'xixi'
