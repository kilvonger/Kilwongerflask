from appist import app
from flask import Flask, flash
from flask import render_template, request

menu = [{'name': 'Главная', 'url': 'index'}, {'name': 'Помощь', 'url': 'help'},
        {'name': 'Обратная связь', 'url': 'contact'}, {'name': 'Отзывы', 'url': 'review'},
        {'name': 'Авторизация', 'url': 'login'}]

@app.route('/')
@app.route('/index')
def index():
    best_ist = {'username': 'Виктория'}
    favorite_writes = [{'author': {'username': 'Tolkien'},
                        'body': ' Lords of the ring'
                        },
                       {'author': {'username': 'Pushkin'},
                        'body': ' Capitans of the daughter'
                        },
                       {'author': {'username': 'Lermontov'},
                        'body': ' Парус'
                        }]

    return render_template('index.html', title='2022 Forever', menu=menu, user=best_ist,
                           foworite_writes=favorite_writes)


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

@app.route('login', methods=['POST','GET'])
def login():
    return render_template('login.html',title='Авторизация', menu=menu)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Внимание страница не найдена', menu=menu, error = error), 404