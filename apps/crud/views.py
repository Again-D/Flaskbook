# db를 import
from flask import Blueprint, redirect, render_template, url_for

# login_required을 import
from flask_login import login_required  # type: ignore

from apps.app import db

# 만들둔 Form 클래스를 import
from apps.crud.forms import UserForm

# User 클래스를 import
from apps.crud.models import User

# Blueprint 객체 생성
crud = Blueprint(
    "crud",
    __name__,
    static_folder="static",
    template_folder="templates",
)


# 맵핑 정보 생성
@crud.route("/")
def index():
    return render_template("crud/index.html")


# 사용자 신규 등록을 위한 엔드포인트 작성
@crud.route("/users/new", methods=["GET", "POST"])
@login_required
def create_user():
    # UserForm 클래스를 인스턴스화
    form = UserForm()
    if form.validate_on_submit():  # submit 클릭시 검증에 문제가 없는 경우.
        # 사용자 정보 생성
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        # DB작업으로 사용자를 추가하고 커밋
        db.session.add(user)
        db.session.commit()

        # 사용자 일람 화면으로 리다이렉트
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)


# 사용자 편집 endpoint
@crud.route("/users/<user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    form = UserForm()

    user = User.query.filter_by(id=user_id).first()

    # form 으로 부터 제출된경우는 사용자를 갱시낳여 사용자의 일람 화면으로 리다이렉트
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))

    # GET의 경우에는 HTML 반환
    return render_template("crud/edit.html", user=user, form=form)


# 사용자 삭제 endpoint
@crud.route("/users/<user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))


# 사용자 일람 endpoint
@crud.route("/users")
@login_required
def users():
    """사용자 일람을 얻는 함수"""
    # users = db.session.query(User).all()
    users = User.query.all()
    return render_template("crud/index.html", users=users)


@crud.route("/sql")
def sql():
    db.session.query(User).all()
    return "콘솔 로그를 확인해주세요"
