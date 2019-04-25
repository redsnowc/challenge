class BaseConfig:
    SECRET_KEY = 'skldflkasf;ajsf;jsdlfa'
    

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
            'mysql+mysqldb://root@shiyanlouhost:3306/simpedu?charset=utf8'
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

