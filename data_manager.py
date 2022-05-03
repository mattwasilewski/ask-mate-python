import os
from datetime import datetime, timezone
from psycopg2 import sql
import database_common

QUESTION_DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
ANSWER_DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


@database_common.connection_handler
def get_questions_desc(cursor, sort_method):
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
        SELECT title, message, submission_time, vote_number, view_number, image
        FROM question
        WHERE id = %s"""
    cursor.execute(query, (question_id,))
    return cursor.fetchone()


@database_common.connection_handler
def get_last_question(cursor):
    query = """
        SELECT * FROM question 
        WHERE id = (SELECT max(id) FROM question)"""
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def get_answers_by_id(cursor, question_id):
    query = """
        SELECT id, message, submission_time, vote_number, image
        FROM answer
        WHERE question_id = %s"""
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


def set_question_data(title, message):
    submission_time = get_current_time()
    view_number = '0'
    vote_number = '0'
    image = None
    add_question_to_database(submission_time, view_number, vote_number, title, message, image)


@database_common.connection_handler
def add_question_to_database(cursor, submission_time, view_number, vote_number, title, message, image):
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
        VALUES (%(time)s, %(view_n)s, %(vote_n)s, %(title)s, %(message)s, %(image)s)
    """
    cursor.execute(query, {'time': submission_time, 'view_n': view_number, 'vote_n': vote_number,
                           'title': title, 'message': message, 'image': image})


@database_common.connection_handler
def edit_question(cursor, question_id, title, message):
    query = """
        UPDATE question 
        SET title = %(new_title)s, message = %(new_message)s
        WHERE id = %(id)s
        """
    cursor.execute(query, {'new_title': title, 'new_message': message, 'id': question_id})


def get_current_time():
    current_time = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    value = datetime.utcfromtimestamp(current_time)
    date_format = f"{value:%Y-%m-%d %H:%M:%S}"
    return date_format


def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


@database_common.connection_handler
def add_answer(cursor, submission_time, vote_number, question_id, message, image):
    query = """
        INSERT INTO answer(submission_time, vote_number, question_id, message, image)
        VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s)
         """
    cursor.execute(query, {'submission_time': submission_time, 'vote_number': vote_number, 'question_id':question_id,
                           'message': message, 'image': image})


@database_common.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    query = """
           SELECT question_id
           FROM answer
           WHERE id = %s"""
    cursor.execute(query, (answer_id,))
    return cursor.fetchone()


@database_common.connection_handler
def delete_question(cursor, question_id):
    query = """
        DELETE
        FROM question
        WHERE id = %s"""
    cursor.execute(query, (question_id,))


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    query = """
        DELETE
        FROM answer
        WHERE id = %s"""
    cursor.execute(query, (answer_id,))