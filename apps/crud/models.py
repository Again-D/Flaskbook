# 날짜 작업을 위해서 사용.
from datetime import datetime

# flask_login내에 UserMixin import
from flask_login import UserMixin

# password_hash 처리를 위한 모듈 import, check_password_hash 추가
from werkzeug.security import check_password_hash, generate_password_hash

# apps.app 모듈에서 db import, 추가 import login_manager
from apps.app import db, login_manager


class User(db.Model, UserMixin):
    # 테이블 이름
    __tablename__ = "users"
    # 컬럼 정의
    id = db.Column(db.Integer, primary_key=True)  # primary_key 속성 부여
    username = db.Column(db.String, index=True)  # index 색인
    email = db.Column(db.String, index=True, unique=True)  # unique, index  설정
    password_hash = db.Column(db.String)
    create_at = db.Column(db.DateTime, default=datetime.now)  # default는 기본값
    update_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )  # onupdate 업데이트시

    # 비밀번호를 설정하기 위한 프로퍼티
    @property
    def password(self):
        raise AttributeError("읽어 들일 수 없음")

    # 비밀번호 설정을 위한 setter
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 비밀번호 체크(패스워드 확인)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 이메일 주소 중복 체크
    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first()

    user_images = db.relationship(
        "UserImage", backref="user", order_by="desc(UserImage.id)"
    )


# 로그인하고 있는 사용자 정보를 얻는 함수를 작성
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)