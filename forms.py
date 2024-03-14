from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, EqualTo, Email, ValidationError

class RegisterForm(FlaskForm):

    def validate_on_submit(self,email_address):
        #logic to check if email is in the DB already
        if email_address == ' ':
            raise ValidationError('This email is already in use!')

    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='submit')


class LoginForm(FlaskForm):
    def validate_on_submit(self, email, pwd):
        #logic to check if email and pwd combo is valid
        if pwd == '':
            return ValidationError('Invalid email or password!')
    
    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    pwd = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Submit')