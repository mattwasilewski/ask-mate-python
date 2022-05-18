import os
from datetime import datetime, timezone
from psycopg2 import sql
import database_common
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'


def save_image_path(file, message, author, question_id=None, title=None):
    filename = ''
    if file.filename != '' and file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        file.save(os.path.join(BASE_PATH + UPLOAD_FOLDER, filename))
    set_answer_data(message, filename, question_id, author) if title is None else set_question_data(title,
                                                                                                    message,
                                                                                                    filename,
                                                                                                    author)


def set_answer_data(message, filename, question_id, author):
    submission_time = get_current_time()
    vote_number = 0
    image = UPLOAD_FOLDER + '/' + filename if filename != '' else None
    add_answer(submission_time, vote_number, question_id, message, image, author)


def set_question_data(title, message, filename, author):
    submission_time = get_current_time()
    view_number = 0
    vote_number = 0
    image = UPLOAD_FOLDER + '/' + filename if filename != '' else None
    add_question_to_database(submission_time, view_number, vote_number, title, message, image, author)


def get_current_time():
    current_time = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    value = datetime.utcfromtimestamp(current_time)
    date_format = f"{value:%Y-%m-%d %H:%M:%S}"
    return date_format


def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


@database_common.connection_handler
def get_questions_desc(cursor, sort_method):
    query = ("""
        SELECT id, title, message, submission_time, view_number, vote_number
        FROM question
        ORDER BY {col} DESC""")
        #todo zamienic na - query nizej tez ORDER BY {col} """ + 'DESC')
    cursor.execute(sql.SQL(query).format(col=sql.Identifier(sort_method)))
    return cursor.fetchall()


@database_common.connection_handler
def get_questions_asc(cursor, sort_method):
    query = ("""
        SELECT id, title, message, submission_time, view_number, vote_number
        FROM question
        ORDER BY {col} ASC""")
    cursor.execute(sql.SQL(query).format(col=sql.Identifier(sort_method)))
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    query = """
        SELECT title, message, submission_time, vote_number, view_number, image, user_id
        FROM question
        WHERE id = %s"""
    cursor.execute(query, (question_id,))
    return cursor.fetchone()


@database_common.connection_handler
def get_answer_message_by_id(cursor, answer_id):
    query = """
        SELECT message
        FROM answer
        WHERE id = %s"""
    cursor.execute(query, (answer_id,))
    return cursor.fetchone()


@database_common.connection_handler
def get_last_question(cursor):
    query = """
        SELECT * FROM question 
        WHERE id = (SELECT max(id) FROM question)"""
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def get_five_latest_questions(cursor):
    query = """
        SELECT * FROM question
        ORDER BY id desc
        LIMIT 5
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_by_id(cursor, question_id):
    query = """
        SELECT answer.id AS id, message, submission_time, vote_number, image, u.username AS author
        FROM answer
        INNER JOIN users u on answer.user_id = u.id
        WHERE question_id = %s
        ORDER BY vote_number desc"""
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@database_common.connection_handler
def add_question_to_database(cursor, submission_time, view_number, vote_number, title, message, image, author):
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
        VALUES (%(time)s, %(view_n)s, %(vote_n)s, %(title)s, %(message)s, %(image)s, %(author_id)s)
    """
    cursor.execute(query, {'time': submission_time, 'view_n': view_number, 'vote_n': vote_number,
                           'title': title, 'message': message, 'image': image, 'author_id': author})


@database_common.connection_handler
def add_comment_to_question(cursor, question_id, message, submission_time, edited_count, author):
    query = """
        INSERT INTO comment (question_id,  message, submission_time, edited_count, user_id)
        VALUES (%(question_id)s, %(message)s, %(submission_time)s,
         %(edited_count)s, %(author_id)s)
        """
    cursor.execute(query, {'question_id': int(question_id), 'message': message, 'submission_time': submission_time,
                           'edited_count': edited_count, 'author_id': author})


@database_common.connection_handler
def edit_question(cursor, question_id, title, message):
    query = """
        UPDATE question 
        SET title = %(new_title)s, message = %(new_message)s
        WHERE id = %(id)s
        """
    cursor.execute(query, {'new_title': title, 'new_message': message, 'id': question_id})


@database_common.connection_handler
def add_answer(cursor, submission_time, vote_number, question_id, message, image, author):
    query = """
        INSERT INTO answer(submission_time, vote_number, question_id, message, image, user_id)
        VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s, %(author_id)s)
         """
    cursor.execute(query, {'submission_time': submission_time, 'vote_number': vote_number, 'question_id': question_id,
                           'message': message, 'image': image, 'author_id': author})


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


@database_common.connection_handler
def delete_answer_by_question_id(cursor, question_id):
    query = """
        DELETE FROM answer WHERE question_id = %s"""
    cursor.execute(query, (question_id,))


@database_common.connection_handler
def delete_comment_by_question_id(cursor, question_id):
    query = """
        DELETE FROM comment WHERE question_id = %s"""
    cursor.execute(query, (question_id,))


@database_common.connection_handler
def increase_question_vote_number_count(cursor, question_id):
    query = """
        UPDATE question
        SET vote_number = vote_number + 1
        WHERE id = %s"""
    cursor.execute(query, (question_id,))


@database_common.connection_handler
def decrease_question_vote_number_count(cursor, question_id):
    query = """
        UPDATE question
        SET vote_number = vote_number - 1
        WHERE id = %s"""
    cursor.execute(query, (question_id,))


@database_common.connection_handler
def increase_answer_vote_number_count(cursor, answer_id):
    query = """
        UPDATE answer
        SET vote_number = vote_number + 1
        WHERE id = %s"""
    cursor.execute(query, (answer_id,))


@database_common.connection_handler
def decrease_answer_vote_number_count(cursor, answer_id):
    query = """
        UPDATE answer
        SET vote_number = vote_number - 1
        WHERE id = %s"""
    cursor.execute(query, (answer_id,))


@database_common.connection_handler
def get_questions_by_searching_phrase(cursor, searching_phrase):
    query = """
        SELECT DISTINCT ON (question.id) question.id , title, question.message as q_message, 
        question.submission_time as q_submission_time, 
        view_number, question.vote_number as q_vote_number, answer.message
        FROM question 
        FULL JOIN answer on question.id = answer.question_id 
        WHERE question.title  ILIKE '%%' || %(phrase)s || '%%' 
        OR question.message ILIKE '%%' || %(phrase)s  || '%%'
        OR answer.message ILIKE '%%' || %(phrase)s  || '%%'
        """
    cursor.execute(query, {'phrase': searching_phrase})
    return cursor.fetchall()


@database_common.connection_handler
def get_all_comments(cursor):
    query = """
        SELECT comment.id, question_id, answer_id, message, submission_time,
               edited_count, u.username AS author
        FROM comment
        INNER JOIN users u on comment.user_id = u.id
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_id_by_question_id(cursor, question_id):
    query = """
        SELECT id FROM answer WHERE question_id = %s"""
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@database_common.connection_handler
def delete_comment_by_answer_id(cursor, answer_id):
    query = """
        DELETE FROM comment WHERE answer_id = %s"""
    cursor.execute(query, (answer_id,))


@database_common.connection_handler
def add_comment_to_answer(cursor, answer_id, message, submission_time, edited_count, author):
    query = """
        INSERT INTO comment (answer_id,  message, submission_time, edited_count, user_id)
        VALUES (%(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s, %(author_id)s)
        """
    cursor.execute(query, {'answer_id': int(answer_id), 'message': message, 'submission_time': submission_time,
                           'edited_count': edited_count, 'author_id': author})


@database_common.connection_handler
def edit_answer(cursor, answer_id, message):
    query = """
        UPDATE answer 
        SET message = %(new_message)s
        WHERE id = %(id)s
        """
    cursor.execute(query, {'new_message': message, 'id': answer_id})


@database_common.connection_handler
def add_user_to_database(cursor, username, password, registration_date):
    query = """
        INSERT INTO users (username,  password, registration_date)
        VALUES (%(username)s, %(password)s, %(registration_date)s)
        """
    cursor.execute(query, {'username': username, 'password': password, 'registration_date': registration_date})


@database_common.connection_handler
def get_users_data(cursor):
    query = """
        SELECT id, username, registration_date FROM users
        ORDER BY id
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_user_data_by_username(cursor, username):
    query = """
        SELECT username, password, registration_date, id FROM users
        WHERE username = %s
        """
    cursor.execute(query, (username,))
    return cursor.fetchone()


@database_common.connection_handler
def get_author_by_id(cursor, user_id):
    query = """
        SELECT username FROM users
        WHERE id = %s
        """
    cursor.execute(query, (user_id,))
    return cursor.fetchone()


@database_common.connection_handler
def count_data_by_user_id(cursor, data):
    query = f"""
        SELECT users.id AS id, COUNT({data}.user_id) AS count_{data}
        FROM users
        FULL JOIN {data} ON {data}.user_id = users.id
        GROUP BY users.id
        ORDER BY users.id
        """
    cursor.execute(query)
    return cursor.fetchall()


#todo jak uzyskac dostep do answer.message
#todo gdy w tytule pytania, jego tresci oraz odpowiedzi jest to samo slowo - wyswietla sie 3 razy
#todo pogrupowac tak by moglo być tylko jedno takie samo question id

#todo podzielic plik wzgledem tabelek