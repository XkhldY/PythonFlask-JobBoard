from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)

PATH = 'db/jobs.sqlite'


@app.route('/')
@app.route('/jobs')
def jobs():
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id,'
                       ' employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template('index.html', jobs=jobs)


def open_connection():
    connection = getattr(g, '_connection', None)
    if connection is None:
        connection = g._connection = sqlite3.connect(PATH)
        connection.row_factory = sqlite3.Row
    return connection


def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.execute(sql, values)
    if commit:
        results = cursor.commit()
    else:
        if single:
            results = cursor.fetchone()
        else:
            results = cursor.fetchall()
    cursor.close()
    return results


@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection:
        connection.close()
