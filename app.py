from flask import Flask, render_template, request, escape
from vsearch import search4letters

app = Flask(__name__)

import mysql.connector

def log_request(req: 'flask_request', res: str) -> None:
    """Журналируем веб-запросы и возвращаем результаты."""
    # with open('vsearch.log', 'a') as log:
    # print(str(dir(req)), res, file=log)
    # print(req.form, file=log, end=' | ')
    # print(req.remote_addr, file=log, end=' | ')
    # print(req.user_agent, file=log, end=' | ')
    # print(res, file=log)
    # print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')

    dbconfig = {'host': '127.0.0.1',
                'user': 'vsearch',
                'password': '1234567890',
                'database': 'vsearchlogDB', }

    conn= mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()

    # with UseDatabase (dbconfig) as cursor:
    _SQL = """insert into log (phrase, letters, ip, browser_string, results) value (%s, %s, %s, %s, %s)"""
    cursor.execute(_SQL, (req.form['phrase'], req.form['letters'], req.remote_addr, req.user_agent.browser, res,))
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/search', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Вот ваш результат:'
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html', the_title=title, the_phrase=phrase, the_letters=letters, the_results=results,)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Добро пожаловать в поиск символов для web!')


@app.route('/viewlog')
def view_the_log() -> 'html':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    title = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html', the_title='View Log', the_row_titles=titles, the_data=contents, )


if '__main__' == __name__:
    app.run(debug=True)