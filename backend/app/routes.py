# backend\app\routes.py
from flask import render_template, redirect, url_for, flash, request, send_file, jsonify
from flask_login import login_user, login_required, logout_user
from app import app
from app.forms import LoginForm, DownloadForm
from app.models import User
from app.utils.downloader import download_and_merge, process_multiple_urls
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/download', methods=['GET', 'POST'])
@login_required
def download():
    if request.method == 'POST':
        urls = request.json.get('urls', '').split('\n')
        output_dir = app.config['UPLOAD_FOLDER']
        results = process_multiple_urls(urls, output_dir)
        return jsonify({'results': results})
    return render_template('download.html')

@app.route('/download_file/<path:filename>')
@login_required
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)
