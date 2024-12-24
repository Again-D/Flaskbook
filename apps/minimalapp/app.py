# os을 import - 시스템 작업을 진행하는 모듈
# logging을 import
import logging
import os

# 이메일 검증 패키지 import
from email_validator import EmailNotValidError, validate_email
# Flask 클래스를 import
from flask import (Flask, current_app, flash, g, make_response, redirect,
                   render_template, request, session, url_for)
# DebugToolbarExtension 확장 import
from flask_debugtoolbar import DebugToolbarExtension
# flask-mail의 Mail 클래스 import
from flask_mail import Mail, Message

# Flask클래스를 인스턴스화 합니다.
app = Flask(__name__)
# __name__ 변수의 값 출력
# print(__name__)

# import random
# import string

# # source 생성
# string_pool = string.ascii_letters + string.digits

# # SECRETKEY
# result = ""
# for i in range(20):
#     result += random.choice(string_pool)
# print(result)

# SECRET_KEY 추가 - session을 위해서 필요함
app.config["SECRET_KEY"] = "VXNA6hHwn5sIuPQpZLxK"

# 로그 레벨 설정
app.logger.setLevel(logging.DEBUG)

# 리다이렉트 중단 하지 않게 설정
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# debugtoolbar 연동 처리..
toolbar = DebugToolbarExtension(app)

# 로그 출력을 위해 다음과 같이 지정
app.logger.critical("fatal error")
app.logger.error("error")
app.logger.warning("warning")
app.logger.info("info")
app.logger.debug("debug")

# Mail 클래스의 config를 추가

# mailserver = os.environ.get("MAIL_SERVER")
# mailport = os.environ.get("MAIL_PORT")
# mailusetls = os.environ.get("MAIL_USE_TLS")
# mailusername = os.environ.get("MAIL_USERNAME")
# mailpassword = os.environ.get("MAIL_PASSWORD")
# maildefaultsender = os.environ.get("MAIL_DEFAULT_SENDER")
# print(mailserver, mailport, mailusetls, mailusername, mailpassword, maildefaultsender)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# flask-mail 확장에 등록(연동)
mail = Mail(app)


# 맵핑... @app.route()
@app.route("/", endpoint="root")
def hello_world():
    return "<h1>Hello, Flask!</h1>"


# template 적용
@app.route("/hello/<name>/<int:out>", methods=["GET", "POST", "PUT"])
def hello(name, out):
    # return f"Hello, {name}!"
    # 템플릿 엔진 적용!!!
    dic = {"name": name, "age": 20, "out": bool(out)}
    # for문을 사용하기 위한 값 생성...
    dataList = []  # user.url, user.username
    user = {}
    for i in range(10):
        user["url"] = f"http://localhost{i}"
        user["username"] = f"testuser{i}"
        dataList.append(user)
        user = {}
    print(dataList)
    return render_template("index.html", data=dic, datas=dataList)


# app.get(), app.post()  플라스크 2.0 이후에 생긴 데코레이터
@app.get("/test", endpoint="getTest")
def testGet():
    return "<h3>testGet</h3>"


@app.post("/test", endpoint="postTest")
def testPost():
    return "<h3>testPost</h3>"


@app.put("/test", endpoint="putTest")
def testPut():
    return "<h3>testPut</h3>"


@app.get("/info/<string:name>/<int:age>", endpoint="testRule")
def testRule(name, age):
    print(type(name), type(age))
    result = f"""<div>
    <h3>info</h3>
    <table border="1">
      <tr><th style="width:100px">이름</th><th style="width:100px">나이</th></tr>
      <tr><td>{name}</td><td>{age}살</td></tr>
    </table>
    </div>"""
    return result


# 요청 컨텍스트 테스트 함수
with app.test_request_context():
    # /
    print('주소 url_for("root") :  ', url_for("root"))  # 주소를 알아오는 함수
    # /test
    print('주소 url_for("putTest") : ', url_for("putTest"))
    # hello :  /hello/test/1
    print("hello : ", url_for("hello", name="test", out=1))
    # hello :  /hello/test/1?page=1&age=10
    # url_for() 사용시, 첫번째 인자는 무조건 endpoint 값을 사용하고,
    # 이후에 있는 값들은 키=값 형태로 지정해주면 Url을 만들어 줍니다.
    print("hello : ", url_for("hello", name="test", out=1, page=1, age=10))
    # info 정보를 출력해보세요!!! URL(출력된 Rule) 확인
    print("info 정보(url) : ", url_for("testRule", name="testinfo", age=10, page=1))

# 여기서 호출하면 오류 생김
# print(current_app)

# 애플리케이션 Context를 취득하여 stack영역에 push
ctx = app.app_context()  # 현재 동작 중인 app의 context를 ctx라는 변수에 저장
ctx.push()  # stack에 저장.

# current_app에 접근 가능
print(current_app.name)

# 전역 임시 영역 값 설정 : (g를 사용하기 위해서는 current_app이 로드되어 있어야 함)
g.connection = "connection"  # connection 정보를 사용하는 내용은 DB접근 정보
print(g.connection)
# g.connect(host='', port=0, timeout=None, source_address=None)

# 요청 Context 테스트
print("요청 컨텍스트 테스트")
with app.test_request_context("/users?updated=true&test=test입니다."):
    # 테스트 결과 출력
    print(request.args.get("updated"))
    print(request.args.get("test"))
    print(request.args)


@app.route("/contact")
def contact():
    session["username"] = "testuser"
    # 응답 객체 생성
    response = make_response(
        render_template("contact.html", username=session["username"])
    )

    # 쿠키 설정
    response.set_cookie("flaskbook_key", "flaskbook_value")

    # 세션 설정
    session["username"] = "testuser"

    # return render_template("contact.html")  # templates내에 contact.html
    return response


@app.route("/contact_complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # request 전달된 값 처리 : form태그로 부터 전달받은 값
        username = request.form["username"]
        email = request.form.get("email")
        description = request.form.get("description")
        # print("username : ", username)
        # print("email : ", email)
        # print("description : ", description)

        # 검증 확인...
        is_valid = True
        if not username:
            flash("사용자명은 필수입니다.")
            is_valid = False
        if not email:
            flash("메일 주소는 필수입니다.")
            is_valid = False

        # 이메일 형식 검증
        try:
            validate_email(email)
        except EmailNotValidError:
            flash("메일 주소 형식으로 입력해 주세요")
            is_valid = False
        if not description:
            flash("문의 내용은 필수입니다.")
            is_valid = False

        # 검증이 실패한 경우 is_valid = False -> 문의 폼으로 되돌림
        if not is_valid:
            app.logger.warning("입력값 검증에 실패입니다.")
            return redirect("contact")

        # 이메일을 발송하기 위한 작업 진행
        print(email, username, description)
        send_email(
            email,
            "문의 감사합니다.",
            "contact_mail",
            username=username,
            description=description,
        )

        # 리다이렉트 처리
        flash("문의해 주셔서 감사합니다.")
        app.logger.info("정상적으로 문의메일를 발송했습니다.")
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")


# 메일 발송과 과련된 함수
def send_email(to, subject, template, **kwargs):
    """메일을 송신하는 함수"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    print(msg)
    mail.send(msg)
