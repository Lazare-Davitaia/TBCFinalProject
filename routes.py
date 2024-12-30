
from flask import render_template, flash, url_for, redirect, request
from flask_wtf import form
from datetime import datetime
from ext import app, db
from models import User, News, University, Like
from forms import RegistrationForm, LoginForm, EditNewsForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
from uuid import uuid4
import logging

# Upload folder
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads/news')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Add UPLOAD_FOLDER to app.config
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please login instead.', 'danger')
            return redirect(url_for('login'))

        new_user = User(username=username, email=email, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Registration successful for {username}', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome {user.username}!', 'success')
            return redirect(url_for('ranking'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)




@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    if current_user.email != 'Lazare26davitaia@gmail.com':
        flash('You are not authorized to add news.', 'danger')
        return redirect(url_for('news_page'))

    form = EditNewsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        image = form.image.data
        date = form.date.data

        if not date:
            date = datetime.utcnow()

        elif isinstance(date, datetime):
            try:
                date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
                return redirect(url_for('add_news'))

        # Save the uploaded image
        if image and allowed_file(image.filename):
            filename = uuid4().hex + os.path.splitext(image.filename)[1]
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None


        new_news = News(title=title, content=content, date=date, image=filename)
        db.session.add(new_news)
        db.session.commit()
        flash('News added successfully!', 'success')
        return redirect(url_for('news_page'))

    return render_template('add_news.html', form=form)


@app.route('/news', methods=['GET'])
@login_required
def news_page():
    news_items = News.query.all()
    return render_template('news_page.html', news=news_items)

@app.route('/like/<int:news_id>', methods=['POST'])
@login_required
def like_news(news_id):
    news_item = News.query.get_or_404(news_id)
    like = Like.query.filter_by(user_id=current_user.id, news_id=news_id).first()

    if like:
        # Remove like if it already exists
        db.session.delete(like)
        db.session.commit()
        return {'status': 'unliked', 'likes': len(news_item.likes)}

    # Add a new like
    new_like = Like(user_id=current_user.id, news_id=news_id)
    db.session.add(new_like)
    db.session.commit()
    return {'status': 'liked', 'likes': len(news_item.likes)}



@app.route('/edit_news/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    news_item = News.query.get_or_404(news_id)

    if current_user.email != 'Lazare26davitaia@gmail.com':
        flash('You are not authorized to edit this news.', 'danger')
        return redirect(url_for('news_page'))

    form = EditNewsForm(obj=news_item)
    if form.validate_on_submit():
        news_item.title = form.title.data
        news_item.content = form.content.data

        # Handle image upload
        image = form.image.data
        if image and hasattr(image, 'filename') and allowed_file(image.filename):
            filename = uuid4().hex + os.path.splitext(image.filename)[1]
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            news_item.image = filename

        db.session.commit()
        flash('News updated successfully!', 'success')
        return redirect(url_for('news_page'))

    app.logger.debug(f"Form errors: {form.errors}")
    return render_template('edit_news.html', form=form, news=news_item)



@app.route('/delete_news/<int:news_id>', methods=['POST'])
@login_required
def delete_news(news_id):
    news_item = News.query.get_or_404(news_id)

    # Check if the current user is authorized to delete the news
    if current_user.email != 'Lazare26davitaia@gmail.com':
        flash('You are not authorized to delete this news.', 'danger')
        return redirect(url_for('news_page'))

    Like.query.filter_by(news_id=news_item.id).delete()

    db.session.delete(news_item)
    db.session.commit()
    flash('News deleted successfully!', 'success')
    return redirect(url_for('news_page'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ranking')
@login_required
def ranking():
    universities = University.query.all()
    return render_template('universities_ranking.html', user=current_user.username, universities=universities)


@app.route('/ranking2')
@login_required
def ranking2():
    universities = University.query.all()
    return render_template('universities_ranking2.html', user=current_user.username)

