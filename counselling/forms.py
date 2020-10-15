from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,TextAreaField,IntegerField
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import DataRequired,ValidationError,Length,Email,EqualTo,Regexp,Required
from counselling.model import User
from flask_login import current_user



# REGISTRATION FORMS
class RegistrationForm(FlaskForm):
    # validators:list will be a list of what we want to check
    first_name = StringField('First Name',validators =[DataRequired(),Length(min=2,max=30) ],render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)],
                           render_kw={"placeholder": "Last Name"})
    mob_number = IntegerField('Mob number', validators=[DataRequired()],
                            render_kw={"placeholder": "Mobile No."})
    email= StringField('Email',validators =[DataRequired(), Email() ],render_kw={"placeholder": "Email"})
    image_file = FileField("Upload Profile Image", validators=[FileAllowed(['jpg', 'png','jpeg'], 'Only jpg,jpeg and png format allowed')],
                         render_kw={"placeholder": "Upload Image"})
    aadhar_file = FileField("Upload AadharCard", validators=[FileAllowed(['jpg', 'png','pdf','jpeg'], 'Only pdf,jpg,jpeg and png format allowed')],
                           render_kw={"placeholder": "Upload AadharCard"})
    ip_address = StringField('IP Address')
    password = PasswordField('Password',validators=[DataRequired()],render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired() ,EqualTo('password') ],render_kw={"placeholder": "Confirm Password"})
    submit =SubmitField('Register')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('The email already exists.Please choose a different one.')

    def validate_mobNo(self, mob_number):
        mob_number = User.query.filter_by(mob_number=mob_number.data).first()
        if mob_number:
            raise ValidationError('The Mobile number already exists.Please choose a different one.')


class LoginForm(FlaskForm):
    # validators:list will be a list of what we want to check
    email= StringField('Email',validators =[DataRequired(), Email() ])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit =SubmitField('Log In')



class UpdateForm(FlaskForm):
    # validators:list will be a list of what we want to check
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)],
                             render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)],
                            render_kw={"placeholder": "Last Name"})
    email = StringField('Email', validators=[DataRequired(), Email()],render_kw={"placeholder": "Email"})
    mob_number = IntegerField('Mob number', validators=[DataRequired()],
                              render_kw={"placeholder": "Mobile No."})
    image_file = FileField('Update Profile picture', validators=[FileAllowed(['jpg', 'png','jpeg'], 'Only jpg,jpeg and png format allowed')])
    submit = SubmitField('Update')


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken.Please choose a different one.')


    def validate_mobNo(self, mob_number):
        if mob_number != current_user.mob_number:
            mob_number = User.query.filter_by(mob_number=mob_number.data).first()
            if mob_number:
                raise ValidationError('The Mobile number already exists.Please choose a different one.')
