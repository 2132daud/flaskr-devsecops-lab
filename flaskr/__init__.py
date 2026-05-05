import os
from flask import Flask, request, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # УЯЗВИМОСТЬ 1: Hardcoded секретный ключ (должен обнаружить Bandit)
    app.config['SECRET_KEY'] = 'super-secret-key-12345-hardcoded-bad-practice'

    # УЯЗВИМОСТЬ 2: Режим отладки всегда включен (потенциальная утечка информации)
    app.config['DEBUG'] = True

    # УЯЗВИМОСТЬ 3: Hardcoded пароль/токен (должен обнаружить Gitleaks)
    ADMIN_PASSWORD = 'admin123!@#password'

    @app.route('/')
    def index():
        # УЯЗВИМОСТЬ 4: Server-Side Template Injection (SSTI)
        name = request.args.get('name', 'Guest')
        # Используем render_template_string вместо render_template
        # Это позволяет внедрять Jinja2 выражения: http://localhost:5000/?name={{7*7}}
        template = f'<h1>Hello {name}!</h1>'
        from flask import render_template_string
        return render_template_string(template)

    @app.route('/eval')
    def eval_endpoint():
        # УЯЗВИМОСТЬ 5: eval() с пользовательским вводом (должен обнаружить Bandit)
        expression = request.args.get('expr', '1+1')
        try:
            # НИКОГДА не используйте eval() с пользовательским вводом!
            result = eval(expression)
            return f'Result: {result}'
        except Exception as e:
            return f'Error: {str(e)}'

    @app.route('/admin')
    def admin():
        # УЯЗВИМОСТЬ 6: Отсутствует проверка авторизации (должен обнаружить ZAP)
        return 'Admin panel - no authentication required!'

    @app.route('/users/<username>')
    def user_profile(username):
        # УЯЗВИМОСТЬ 7: Отсутствует валидация ввода и экранирование
        return f'<h1>Profile of {username}</h1>'

    @app.route('/search')
    def search():
        # УЯЗВИМОСТЬ 8: Потенциальная XSS (Cross-Site Scripting)
        query = request.args.get('q', '')
        return f'''
            <h1>Search Results</h1>
            <p>You searched for: {query}</p>
            <p>No results found.</p>
        '''

    return app