from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BookForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    author = StringField('Autor', validators=[DataRequired()])
    genre = StringField('Género', validators=[DataRequired()])
    year = IntegerField('Año de Publicación', validators=[DataRequired(), NumberRange(min=0)])
    rating = FloatField('Calificación Promedio', validators=[DataRequired(), NumberRange(min=0, max=5)])
    pages = IntegerField('Número de Páginas', validators=[DataRequired()])
    price = FloatField('Precio (USD)', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    is_admin = BooleanField('Admin') 
    submit = SubmitField('Register')
