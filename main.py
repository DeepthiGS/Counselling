from flask import Flask, render_template, flash,redirect,url_for,request
import secrets,os
from PIL import Image
from counselling.forms  import RegistrationForm,UpdateForm,LoginForm
from flask_login import  current_user,login_user,login_required,logout_user
from counselling import  app,db,bcrypt
from counselling.model import User

# Sample data

# details =[
#     {
#         "name" : "Deepthi Shettigar",
#         "mobile_number" : 98932434244,
#         "email-id": "deepthi@gmail.com",
#         "image_file": "default.jpg"
#
#     },
#     {
#         "name": "Shrushti Dhurve",
#         "mobile_number": 98932434244,
#         "email-id": "shrushtid@gmail.com",
#         "image_file": "default.jpg"
#
#     }
# ]

@app.route("/home")
def home():
    query = request.args.get('query')
    if query:
        user = User.query.filter(User.first_name.contains(query) | User.last_name.contains(query) | User.mob_number.contains(query))
    else:
        user= User.query.filter_by().order_by(User.date_register.desc()).all()
    return render_template('index.html', title="HOME",user=user)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ ,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pic' ,picture_fn)

    output_size =(125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return  picture_fn

def save_image(form_picture):
    random_hex = secrets.token_hex(8)
    _ ,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/adhar_images' ,picture_fn)

    output_size =(280,555)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return  picture_fn



@app.route("/register",methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            current_user.image_file = picture_file
            add_file =save_image(form.aadhar_file.data)
            current_user.aadhar_file =add_file
            user = User(first_name = form.first_name.data ,last_name = form.last_name.data,mob_number=form.mob_number.data,email = form.email.data,
                        image_file=current_user.image_file,
                    aadhar_file=current_user.aadhar_file ,ip_address =str(request.remote_addr), password = hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Your account has been created. You are now able to login', 'success')
            return redirect(url_for('login'))
        else:
            user = User(first_name = form.first_name.data ,last_name = form.last_name.data,mob_number=form.mob_number.data,email = form.email.data ,ip_address =str(request.remote_addr), password = hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Your account has been created. You are now able to login', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', title="Register", form=form)


@app.route("/login",methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user,remember=form.remember.data)
			next_page = request.args.get(url_for('update'))
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash(f'Login Unsuccessful.Please check the email and the password.','danger')
		return redirect(url_for('login'))
	return render_template('login.html',form =form,title="Login")



@login_required
@app.route("/update",methods=['GET','POST'])
def update():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            current_user.image_file = picture_file
            # this is used to bring the form already filled in
        current_user.first_name=form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.mob_number = form.mob_number.data
        db.session.commit()
        flash('Your account has been updated! ', 'success')
        return redirect(url_for('update'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data =   current_user.email
        form.mob_number.data = current_user.mob_number
    image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
    return render_template('update.html',title="Update Account",image_file=image_file,form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route("/delete/<int:user_id>",methods=['GET','POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('home'))


app.run()
