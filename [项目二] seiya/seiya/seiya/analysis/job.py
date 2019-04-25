from seiya.db.job import Job, session
from sqlalchemy.sql import func


def analysis_top10_city():
    city_list = session.query(
                Job.city, func.count(Job.city)).group_by(
                Job.city).order_by(func.count(Job.city).desc()).all()
    data = [{'name': i[0], 'amount': i[1]} for i in city_list][:10]
    return data


def analysis_top10_wage():
    salary_list = session.query(Job.city, func.avg(
            (Job.salary_upper+Job.salary_lower)/2)).group_by(
            Job.city).order_by(func.avg(
            (Job.salary_upper + Job.salary_lower) / 2).desc()).all()
    data = [{'name' : i[0], 'salary': float(i[1])}
            for i in salary_list][:10]
    return data

