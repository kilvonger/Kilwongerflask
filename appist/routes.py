import datetime
from os import abort
import sqlite3
from appist import app
from flask import Flask, flash, session, redirect, url_for, g
from flask import render_template, request

from appist.bd_ac import FDataBase

menu = [{'name': 'Главная', 'url': 'index'}, {'name': 'Помощь', 'url': 'help'},
        {'name': 'Обратная связь', 'url': 'contact'}, {'name': 'Отзывы', 'url': 'review'},
        {'name': 'Авторизация', 'url': 'login'},{'name':'Главная БД','url':'/db/index_db'}]

users = [{'user': 'user', 'psw': 'pswrd'}]
app.permanent_session_lifetime = datetime.timedelta(seconds=120)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    '''Cоединение с БД, если она еще не установлена'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    '''Закрытие соединения с БД, если оно есть '''
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route('/db/index_db')
def index_db():
    db = get_db()
    db = FDataBase(db)
    return render_template('index_db.html', title = '2022 Forever', menu = db.getMenu())

@app.route('/db/feedback')
def feedback():
    return render_template('index_db.html', title = '2022 Forever', menu = [])


@app.route('/index')
def index():

    return render_template('index.html', title = '2022 Forever', menu = menu)

@app.route('/help')
def help():
    return render_template('help.html', menu=menu, title='Помощь')

@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        if len(request.form['username']) >=2:
            flash('Сообщение отправлено', category='success')
            print(request.form)
            print(request.form['username'])
        else:
            flash("Ошибка отправки", category='error')
    return render_template('contact.html', title=' Контакт', menu=menu)
@app.route('/about')
def about():
    return render_template('about.html', menu=menu, title='Информация')
@app.route('/review')
def review():
    return render_template('review.html', menu=menu, title='Отзывы')

@app.route('/login', methods=['POST','GET'])
def login():
    if 'userlogged' in session:
        return redirect(url_for('profile', username=session['userlogged']))
    elif request.method == "POST" and len (request.form['username']) > 4 and len(request.form['psw']) > 4:
        session ['userlogged'] = request.form['username']
        users.append({'user':request.form['username'], 'psw': request.form['psw']})
        print(users)
        return redirect(url_for('profile', username=session['userlogged']))
    elif request.method == "POST" and len(request.form['username']) < 4 and len(request.form['psw']) < 4:
        flash("Ошибка создания", category='error')
    return render_template('login.html',title='Авторизация', menu=menu)
@app.route('/profile/<username>')
def profile(username):
    if 'userlogged' not in session or ['userlogged'] != username:
        abort(401)
    return f"<h3> Пользователь: {username} </h3> " \
        f"<a href=""{{ url_for('login') }}""> Вернуться назад </a>"

@app.errorhandler(401)
def unauthorized(error):
    return render_template('page401.html', title='Внимание отказано в доступе', menu=menu, error=error), 401
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Внимание страница не найдена', menu=menu, error = error), 404