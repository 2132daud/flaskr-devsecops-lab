import os
from flask import Flask, request, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # ИСПРАВЛЕНИЕ 1: Секретный ключ теперь берется из переменной окружения.
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))

    # ИСПРАВЛЕНИЕ 2: Режим отладки управляется переменной окружения.
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False') == 'True'

    @app.route('/')
    def index():
        # ИСПРАВЛЕНИЕ 3: Больше нет уязвимости SSTI.
        name = request.args.get('name', 'Guest')
        return render_template('index.html', name=name)

    # ИСПРАВЛЕНИЕ 4: Полностью убрали маршрут /eval, так как eval() - это зло.

    @app.route('/admin')
    def admin():
        # ИСПРАВЛЕНИЕ 5: Добавлена простейшая проверка по токену.
        auth_token = request.headers.get('Authorization')
        expected_token = os.environ.get('ADMIN_TOKEN')
        if not auth_token or auth_token != f'Bearer {expected_token}':
            return 'Unauthorized', 401
        return 'Admin panel'

    return app