from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql://root@localhost/seiya?charset=utf8')
Base = declarative_base(engine)
session = sessionmaker(engine)()

class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    title = Column(String(64))
    city = Column(String(16))
    salary_lower = Column(Integer)
    salary_upper = Column(Integer)
    experience_lower = Column(Integer)
    experience_upper = Column(Integer)
    education = Column(String(16))
    tags = Column(String(256))
    company = Column(String(32))


if __name__ == '__main__':
    Base.metadata.create_all()
