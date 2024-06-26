from flask import Flask , render_template , flash , request , redirect , url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField , PasswordField , BooleanField , ValidationError
from wtforms.validators import DataRequired , EqualTo , Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime , date
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash , check_password_hash
from wtforms.widgets import TextArea
from flask_login import UserMixin , login_user , LoginManager , login_required , logout_user , current_user
#create a flask instance
app = Flask(__name__)
#create a secret key---
app.config['SECRET_KEY'] = "my first final project"


#add a database
#sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#initialise the database
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#create a json thing
@app.route('/data')
def get_current_date():
    return {"Date": date.today()}

#create a blog post model
class Posts(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    shopname = db.Column(db.String(100))
    content = db.Column(db.Text)
    shopowner = db.Column(db.String(100))
    address = db.Column(db.String(150))
    contact = db.Column(db.String(10))
    date_posted = db.Column(db.DateTime ,default = datetime.utcnow)
    slug = db.Column(db.String(150))

#create model
class Users(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(25),nullable = False , unique = True)
    name = db.Column(db.String(100) , nullable = False)
    email = db.Column(db.String(150) , nullable = False , unique = True )
    hometown = db.Column(db.String(120) , nullable = False )  
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    #adding passwords
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self,password):
       return check_password_hash(self.password_hash , password)
    #create a string
    def __repr__(self):
        return '<Name %r>' % self.name


#create a form class
class UserForm(FlaskForm):
    name = StringField("Name", validators = [DataRequired()])
    username = StringField("username" , validators=[DataRequired()])
    email = StringField("Email",validators = [DataRequired()])
    hometown = StringField("HomeTown", validators=[DataRequired()])
    password_hash = PasswordField('Password' , validators = [DataRequired(), EqualTo('password_hash2', message = 'Passwords must match')])
    password_hash2 =  PasswordField('Comfirm password', validators = [DataRequired()] )
    submit = SubmitField("Submit")

#update class form
class UpdateForm(FlaskForm):
    name = StringField("Name", validators = [DataRequired()])
    username = StringField("username", validators=[DataRequired()])
    email = StringField("Email",validators = [DataRequired()])
    hometown = StringField("HomeTown",validators= [DataRequired()])
    password_hash = PasswordField('Password' , validators = [DataRequired(), EqualTo('password_hash2', message = 'passwords must match')])
    password_hash2 =  PasswordField('Comfirm password', validators = [DataRequired()] )
    update = SubmitField("update")

#create a form class
class namerform(FlaskForm):
    name = StringField("Your name", validators = [DataRequired()])
    submit = SubmitField("Submit")

#create a password form
class PasswordForm(FlaskForm):
    email = StringField("Your email?", validators = [DataRequired()])
    password_hash = PasswordField("whats your password?",validators=[DataRequired()])
    submit = SubmitField("Submit")

#create a posts form
class PostForm(FlaskForm):
        shopname = StringField("shopname", validators=[DataRequired()] )
        content = StringField("content",validators=[DataRequired()],widget = TextArea())
        shopowner = StringField("shopowner",validators=[DataRequired()])
        address = StringField("address",validators=[DataRequired()])
        contact = StringField("contact",validators= [Length(min=10, max=10, message="Telephone should be 10 digits (no spaces)")])
        slug = StringField("slug")
        submit = SubmitField("Submit")

#create login form
class LoginForm(FlaskForm):
      username = StringField("username", validators=[DataRequired()])
      password = PasswordField("password",validators=[DataRequired()])
      submit = SubmitField("Submit")

#flask login 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


#create a route decorator
@app.route('/')
#def index():
#  return "<h1>hello world</h1>"
def index():
    flash("welcome to MarketMaven.com !!")
    first_name = "vishnu vardhan"
    fav_food = ["pasta","jelly","flask"]
    return render_template("index.html",first_name = first_name,fav_food = fav_food)


#localhost:5000/user/vishnu
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name = name)

@app.route('/user/add',methods = ["GET","POST"] )
def add_user():
    name = None
    username = None
    hometown = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            #hashing the password
            hashed_pw = generate_password_hash(form.password_hash.data , "pbkdf2:sha256")
            user = Users(name = form.name.data ,username = form.username.data , email = form.email.data , hometown = form.hometown.data , password_hash = hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash('User added successfully!')
        else:
            flash('email already exists. Try with another email')
    name = form.name.data
    hometown = form.hometown.data
    form.name.data = ''
    form.username.data = ''
    form.email.data = ''
    form.hometown.data = ''
    form.password_hash.data = ''
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form = form , name = name ,hometown = hometown, username = username ,our_users = our_users)

@app.route('/update/<int:id>', methods = ['GET','POST'])
def update(id):
    form = UpdateForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.hometown = request.form['hometown']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User updated successfully")
            return render_template("update.html", form = form , name_to_update = name_to_update , id = id)
        except:
            flash("error! try again")
            return render_template("update.html", 
				form=form,
				name_to_update = name_to_update,
				id=id)
    else:
        return render_template("update.html", form = form , name_to_update = name_to_update , id = id)
        
@app.route("/delete/<int:id>")
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    hometown = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("user deleted successfully!!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form = form , name = name ,hometown = hometown, our_users = our_users)

    except:
        flash("whoops! try again to delete ")
        return render_template("add_user.html", form = form , name = name ,hometown = hometown, our_users = our_users)

#create namepage
@app.route('/name',methods = ['GET','POST'])
def name():
    name = None
    form = namerform()
    #validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("form submitted successfully")
    return render_template("name.html",name = name,form = form)

#create password test page
@app.route('/test_pw',methods = ['GET','POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    #validate form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ''
        form.password_hash.data = ''
        #search user by email address
        pw_to_check = Users.query.filter_by(email = email).first()
        #check hashed password
        passed = check_password_hash(pw_to_check.password_hash,password)

    return render_template("test_pw.html",email = email,password = password,pw_to_check = pw_to_check,passed = passed ,form = form)

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html',post = post)

@app.route('/posts/edit/<int:id>', methods = ['GET','POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.shopname = form.shopname.data
        post.shopowner = form.shopowner.data
        post.content = form.content.data
        post.address = form.address.data
        post.slug = form.slug.data
        post.contact = form.contact.data
        #update database
        db.session.add(post)
        db.session.commit()
        flash("offer is updated!")
        return redirect(url_for('post',id = post.id))
    form.shopname.data = post.shopname 
    form.shopowner.data = post.shopowner 
    form.content.data = post.content 
    form.address.data = post.address 
    form.slug.data = post.slug 
    form.contact.data = post.contact 
    return render_template('edit_post.html' , form = form)
#add post page
@app.route('/add-post',methods = ['GET','POST'])
#@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(shopname = form.shopname.data , content = form.content.data , shopowner = form.shopowner.data , address = form.address.data ,slug = form.slug.data , contact = form.contact.data)
        form.shopname.data = ''
        form.contact.data = ''
        form.shopowner.data = ''
        form.address.data = ''
        form.slug.data = ''
        form.content.data = ''
        #add post to database
        db.session.add(post)
        db.session.commit()
        flash("Posted successfully!")
    return render_template("add_post.html" , form = form)

#delete a post
@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        #return a message
        flash("Your post has been deleted.")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts = posts)
    except:
        flash("error try again")

@app.route('/posts')
def posts():
    #grab al offers from database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts = posts)


#create a login page
@app.route('/login',methods =['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username = form.username.data).first()
        if user:
            #check the password
            if check_password_hash(user.password_hash , form.password.data):
                login_user(user)
                flash("login successfull")
                return redirect(url_for('dashboard'))
            else:
                flash("wrong password - try again")
        else:
            flash("Username doesnt exist. Try again ")

    return render_template('login.html',form = form)

#create a logout page
@app.route('/logout',methods =['GET','POST'] )
@login_required
def logout():
    logout_user()
    flash("you have loged out ")
    return redirect(url_for('login'))


#create dashboard page
@app.route('/dashboard',methods =['GET','POST'])
@login_required
def dashboard():
    form = UpdateForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.hometown = request.form['hometown']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User updated successfully")
            return render_template("dashboard.html", form = form , name_to_update = name_to_update , id = id)
        except:
            flash("error! try again")
            return render_template("dashboard.html", 
				form=form,
				name_to_update = name_to_update,
				id=id)
    else:
        return render_template("dashboard.html", form = form , name_to_update = name_to_update , id = id)
        
   

#create custom pages
#invalid URL
@app.errorhandler(404)

def page_not_found(e):
    return render_template("404.html"),404

#internal server error
@app.errorhandler(500)

def page_not_found(e):
    return render_template("500.html"),500