import os
from datetime import datetime, timezone
import csv
from flask import request
from werkzeug.utils import secure_filename
from psycopg2 import sql
import database_common

QUESTION_DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
ANSWER_DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
BASEPATH = os.path.dirname(os.path.abspath(__file__)) + '/'

#todo do wyrzucenia
def get_data(datafile):
    with open(datafile) as csvfile:
        reader = csv.DictReader(csvfile)
        items = [dict(story) for story in reader]
        return items

#todo do wyrzucenia
def convert_data(datafile):
    converted_data = get_data(datafile)
    for row in converted_data:
        value = datetime.utcfromtimestamp(int(row['submission_time']))
        row['submission_time'] = f"{value:%Y-%m-%d %H:%M:%S}"
    return converted_data

#todo do wyrzucenia
def convert_questions():
    return convert_data(QUESTION_DATA_FILE_PATH)

#todo do wyrzucenia
def get_converted_question(question_id):
    for row in convert_questions():
        if row['id'] == question_id:
            return row


@database_common.connection_handler
def get_questions_desc(cursor, sort_method):
    print(sql.Identifier(sort_method))
    query = ("""
        SELECT id, title, message, submission_time, view_number, vote_number
        FROM question
        ORDER BY {col} desc""")
    cursor.execute(sql.SQL(query).format(col=sql.Identifier(sort_method)))
    return cursor.fetchall()


@database_common.connection_handler
def get_questions_asc(cursor, sort_method):
    query = ("""
        SELECT id, title, message, submission_time, view_number, vote_number
        FROM question
        ORDER BY {col} asc""")
    cursor.execute(sql.SQL(query).format(col=sql.Identifier(sort_method)))
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    query = """
        SELECT title, message, submission_time, vote_number, view_number
        FROM question
        WHERE id = %s"""
    cursor.execute(query, (question_id,))
    return cursor.fetchone()


def get_converted_answers(question_id):
    answers = []
    for row in convert_answers():
        if row['question_id'] == question_id:
            answers.append(row)
    return answers


def convert_answers():
    return convert_data(ANSWER_DATA_FILE_PATH)


def save_new_answer(new_answer):
    data_file = open(ANSWER_DATA_FILE_PATH, 'a', newline='')
    fieldnames = ANSWER_HEADERS
    writer = csv.DictWriter(data_file, fieldnames=fieldnames)
    writer.writerow(new_answer)


def save_updated_data(updated_data):
    csvfile = open(QUESTION_DATA_FILE_PATH, 'w', newline='')
    fieldnames = QUESTION_HEADERS
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for story in updated_data:
        writer.writerow(story)


def get_current_time():
    current_time = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    return current_time


def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def add_answer(question_id, message):
    answer = {}
    filename = ''
    if 'question-image' in request.files:
        file = request.files['question-image']
        if file.filename != '' and file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file.save(os.path.join(BASEPATH + UPLOAD_FOLDER, filename))
    answer['id'] = len(get_answers()) + 1
    answer['submission_time'] = get_current_time()
    answer['vote_number'] = '0'
    answer['question_id'] = question_id
    answer['message'] = message
    answer['image'] = UPLOAD_FOLDER + '/' + filename
    save_new_answer(answer)


def update_question(question_id, title, message):
    updated_data = []
    for row in get_questions():
        if row['id'] == question_id:
            row['title'] = title
            row['message'] = message
            row['submission_time'] = get_current_time()
        updated_data.append(row)
        save_updated_data(updated_data)


def get_answers():
    return get_data(ANSWER_DATA_FILE_PATH)


def get_answer(question_id):
    answers = get_answers()
    for row in answers:
        if row['question_id'] == question_id:
            return row


def get_questions():
    return get_data(QUESTION_DATA_FILE_PATH)


def get_question(question_id):
    questions = get_questions()
    for row in questions:
        if row['id'] == question_id:
            return row
