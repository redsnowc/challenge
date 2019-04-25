from seiya.db.job import Job, session
from sqlalchemy.sql import func


def analysis_top10_city():
    city_list = session.query(Job.city, func.count(Job.city)).group_by(Job.city).all()
    city_list = sorted(city_list, key=lambda i: i[1], reverse=True)[:10]
    data = [{'name': i[0], 'amount': i[1]} for i in city_list]
    return data

def analysis_top10_wage():
    salary_list = session.query(
            Job.city, func.avg(Job.salary_upper), 
            func.avg(Job.salary_lower)).group_by(Job.city).all()
    slary_list = [
            {'name' : i[0], 'salary': float((i[1] + i[2]) / 2)} 
            for i in salary_list]
    data = sorted(slary_list, key=lambda i: i['salary'], reverse=True)[:10]
    return data

