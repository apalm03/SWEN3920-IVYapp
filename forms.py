from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    image = FileField('Photo', validators=[
    FileRequired(),
    FileAllowed(['jpg', 'png', 'Images only!'])
    ])
    
