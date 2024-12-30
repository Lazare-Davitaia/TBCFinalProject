from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, FileField
from wtforms.validators import DataRequired, Email, Length, equal_to


# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=4, max=150)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        'confirm_Password',
        validators=[DataRequired(),equal_to('password')]
    )
    submit = SubmitField('Register')


# Login Form
class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    submit = SubmitField('Login')


# Edit News Form
class EditNewsForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired()]
    )
    content = TextAreaField(
        'Content',
        validators=[DataRequired()]
    )
    date = DateField(
        'Date',
        format='%Y-%m-%d',
        validators=[]
    )
    image = FileField('Image')
    submit = SubmitField('Save Changes')
