from app import *
from flask import render_template, flash, redirect, url_for, session, request
from wtforms import Form, StringField, TextAreaField, PasswordField
from passlib.hash import sha256_crypt

class RegiserForm(Form):
        name = StringField()
        username = StringField()
        email = StringField()
        password = PasswordField()
        confirm = PasswordField()

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegiserForm(request.form)

    if request.method == 'POST':
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        mysql.connection.commit()

        cur.close()

        flash('You are now registered please login', 'sucess')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            data = cur.fetchone()
            password = data['password']

            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))

            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

class RegiserForm(Form):
        title = StringField()
        body = TextAreaField()

@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    return render_template('add_article.html')
    form = ArticleForm(request.form)
    if request.method == 'POST':
        title = form.title.data
        body = form.body.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)", (title, body, session['username']))

        mysql.connection.commit()

        cur.close()

        flash('Article created', 'sucess')

        return redirect(url_for('dashboard'))

    return render_template('add_article', form=form)
