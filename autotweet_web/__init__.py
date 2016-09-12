import logging
import os
from flask import Flask, g, jsonify, render_template, request
from autotweet.learning import DataCollection

__version__ = '0.1.0'

app = Flask(__name__)

logger = logging.getLogger('web')


@app.before_first_request
def initialize():
    app.config['DB_URI'] = app.config.get('DB_URI', None) or\
        os.getenv('DATABASE_URL')

    log_file = app.config.get('LOG_FILE', None)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        logger.addHandler(file_handler)

    global data_collection;
    data_collection = DataCollection(app.config['DB_URI'])


@app.route('/')
def form():
    count = data_collection.get_count()
    return render_template('form.html', count=count)


@app.route('/query/')
def result():
    query = request.args['query']
    result = data_collection.get_best_answer(query)
    if not result:
        r = jsonify()
        r.status_code = 404
        return r

    answer, ratio = result

    logger.info(u'{0} -> {1} ({2})'.format(query, answer, ratio))

    return jsonify({
        'answer': answer,
        'ratio': ratio,
        })


@app.route('/teach/', methods=['POST'])
def teach():
    question = request.form['question'].strip()
    answer = request.form['answer'].strip()

    if question and answer:
        data_collection.add_document(question, answer)
        return ''

    return ('', 400)
