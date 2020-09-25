from flask                         import Flask
from flask_cors                    import CORS
from sqlalchemy                    import create_engine
from sqlalchemy.pool               import QueuePool
from sqlalchemy.orm                import sessionmaker

from model                         import ProductDao, UserDao
from service                       import ProductService, UserService
from controller                    import create_product_endpoints, create_user_endpoints

def create_app(test_config = None):
    app = Flask(__name__)
    
    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.update(test_config)
        
    # DB 연결
    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', pool_size = 1000, max_overflow = 100, poolclass = QueuePool)
    
    # database와 연동된 session maker 생성, connection 필요시마다 session instace 생성
    Session = sessionmaker(bind = database)

    # CORS 설정
    CORS(app, resources = {r'*' : {'origins': '*'}})
    
    # Persistance layer
    user_dao    = UserDao()
    product_dao = ProductDao()
    
    # Business layer
    user_service    = UserService(user_dao)
    product_service = ProductService(product_dao)
    
    # Presentation layer
    app.register_blueprint(create_user_endpoints(user_service, Session))
    app.register_blueprint(create_product_endpoints(product_service, Session))
    
    return app