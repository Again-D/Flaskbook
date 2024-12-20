from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField

class UploadImageForm(FlaskForm):
    # 파일 업로드에 필요한 유효성 검증을 설정한다
    image =