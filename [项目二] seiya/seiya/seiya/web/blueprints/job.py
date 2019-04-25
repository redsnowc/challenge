from flask import Blueprint, render_template, jsonify
from seiya.analysis.job import analysis_top10_city, analysis_top10_wage


job_bp = Blueprint('job', __name__, url_prefix='/job')

@job_bp.route('/')
def index():
    return render_template('job/index.html')

@job_bp.route('/top10-city')
def top10_city():
    data = analysis_top10_city()
    return render_template('job/top10_city.html', city_data=data)

@job_bp.route('/top10-wage')
def top10_wage():
    data = analysis_top10_wage()
    return render_template('job/top10_wage.html', salary_data=data)
