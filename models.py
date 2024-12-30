
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ext import db,login_manager



# User Model
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)






    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)



class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime)



class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)

    user = db.relationship('User', backref='likes', lazy=True)
    news = db.relationship('News', backref='likes', lazy=True)





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# University Model
class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(150), nullable=False)  # University name
    rank = db.Column(db.Integer, nullable=False)  # University rank
    location = db.Column(db.String(100), nullable=False)  # Location of the university
    founded = db.Column(db.Integer, nullable=False)  # Year founded
    programs_offered = db.Column(db.String(200), nullable=True)  # Programs offered (optional)
    tuition_fee_min = db.Column(db.Float, nullable=True)  # Minimum tuition fee (optional)
    tuition_fee_max = db.Column(db.Float, nullable=True)  # Maximum tuition fee (optional)
    website = db.Column(db.String(100), nullable=True)  # Website URL (optional)
    logo_url = db.Column(db.String(200), nullable=True)  # Logo URL (optional)

