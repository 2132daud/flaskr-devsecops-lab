import os
from flask import Flask, request, render_template_string

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # УЯЗВИМОСТЬ 1: Hardcoded secret key
    app.config['SECRET_KEY'] = 'hardcoded-secret-key-12345'

    # УЯЗВИМОСТЬ 2: Debug mode enabled
    app.config['DEBUG'] = True

    @app.route('/')
    def index():
        # УЯЗВИМОСТЬ 3: SSTI (Server-Side Template Injection)
        name = request.args.get('name', 'Guest')
        template = f'<h1>Hello, {name}!</h1><p>Welcome to Flaskr</p>'
        return render_template_string(template)

    @app.route('/eval')
    def eval_code():
        # УЯЗВИМОСТЬ 4: Code injection через eval
        expression = request.args.get('expr', '1+1')
        result = eval(expression)
        return f'Result: {result}'

    @app.route('/admin')
    def admin():
        # УЯЗВИМОСТЬ 5: Отсутствие аутентификации для админ-панели
        return 'Admin panel - No authentication!'

    return app