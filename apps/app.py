# 경로 작업
from pathlib import Path

from flask import Flask, render_template

# flask-login에 있는 LoginManager를 import
from flask_login import LoginManager

# 마이그레이션 작업을 위해
from flask_migrate import Migrate  # type: ignore

# SQL작업을 위해
from flask_sqlalchemy import SQLAlchemy

# flask-wtf 모듈의 CSRFProtect import
from flask_wtf.csrf import CSRFProtect  # type: ignore

# config 모듈을 import
from apps.config import config

# LoginManager 객체 생성(*)
login_manager = LoginManager()
# login_view 속성에 미로그인시 리다이렉트하는 엔드포인트를 지정
login_manager.login_view = "auth.login"
# login_message 속성 : 로그인시 표시할 메시지를 지정. 현재는 표시할 내용없어서 ""
# login_message는 기본값으로 설정되어 있어요. 영어로 값이 이미 존재함.
login_manager.login_message = ""

# SQLAlchemy 객체 생성
db = SQLAlchemy()

# CSRFProtect 객체 생성
csrf = CSRFProtect()


# create_app 함수 작성
def create_app(config_key):
    # 플라스크 인스턴스 생성
    app = Flask(__name__)

    # app에 config 설정
    # app에 config 설정- from_object를 이용
    app.config.from_object(config[config_key])

    # csrf 앱 연계
    csrf.init_app(app)

    # SQLAlchemy와 앱 연계
    db.init_app(app)
    # Migrate와 앱 연계
    Migrate(app, db)

    # login_manager를 app과 연계(*)
    login_manager.init_app(app)

    # CRUD패키지로 부터 views 모듈을 import 한다.
    # views.py 모듈은 @app.route()와 같은 맵핑 기능을 가진 모듈
    from apps.crud import views as crud_views  # as 이후 별칭 선언

    # register_blueprint() 사용해 views(crud_views) blueprint에 등록
    # 엔드포인트 앞에 crud가 붙게 됨.
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    # AUTH 패키지로 부터 views 모듈을 import
    from apps.auth import views as auth_views

    # register_blueprint()로 blueprint 등록
    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    # 이제부터 작성하는 detector 패키지로부터 views를 import 한다
    from apps.detector import views as dt_views

    # register_blueprint를 사용해 views의 dt를 앱에 등록한다
    app.register_blueprint(dt_views.dt)

    # 커스텀 오류 화면을 등록한다
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    return app


def page_not_found(e):
    """404 Not FOund"""
    return render_template("404.html"), 404


def internal_server_error(e):
    """500 Internal Server Error"""
    return render_template("500.html"), 500