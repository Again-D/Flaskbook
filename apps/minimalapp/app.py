from flask import Flask

# create_app 함수 작성
def create_app():
    app = Flask(__name__)
    
    from app.crud import views as crud_views
    
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    
    return app

