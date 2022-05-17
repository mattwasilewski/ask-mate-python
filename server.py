from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash
from dotenv import load_dotenv
from bonus_questions import SAMPLE_QUESTIONS
import data_manager
import util
import os
import bcrypt

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def validate_login(username, password):
    userdata = data_manager.get_user_data_by_username(username)
    if userdata and verify_password(password, userdata.get('password')):
        session['username'] = username
        flash('You were successfully logged in!', 'success')
        return redirect(url_for('main_page'))


@app.route("/")
def main_page():
    questions = data_manager.get_five_latest_questions()
    return render_template('main-page.html', questions=questions, username=session.get('username'))


@app.route("/search")
def search_questions():
    searching_phrase = request.args.get('q')
    questions = data_manager.get_questions_by_searching_phrase(searching_phrase)
    return render_template('search-questions.html', searching_phrase=searching_phrase, questions=questions)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        if 'question-image' in request.files:
            data_manager.save_image_path(request.files['question-image'], request.form.get('message'), None,
                                         request.form.get('title'))
        question_id = data_manager.get_last_question()['id']
        return redirect(url_for('display_question', question_id=question_id))
    elif not session.get('username'):
        flash("You need to be logged in to access this page.", 'warning')
        return redirect(url_for('main_page'))
    return render_template('add-question.html', username=session.get('username'))


@app.route("/list")
def route_list():
    sort_method = request.args.get('order_by')
    order = request.args.get('order_direction')
    question = util.get_sorted_questions(sort_method, order)
    return render_template('list.html', questions=question, username=session.get('username'))


@app.route("/question/<question_id>")
def display_question(question_id):
    comments = data_manager.get_all_comments()
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_id(question_id)
    return render_template('question.html', answers=answers, question=question,
                           question_id=question_id, comments=comments,
                           username=session.get('username'))


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def new_answer(question_id):
    if request.method == 'POST':
        if 'question-image' in request.files:
            data_manager.save_image_path(request.files['question-image'], request.form.get('message'), question_id)
        return redirect(url_for('display_question', question_id=question_id))
    elif not session.get('username'):
        flash("You need to be logged in to access this page.", 'warning')
        return redirect(url_for('main_page'))
    return render_template('answer.html', question_id=question_id)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("static", filename)


@app.route("/question/<question_id>/edit", methods=['POST', 'GET'])
def edit_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'POST':
        data_manager.edit_question(question_id, request.form['title'], request.form['message'])
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('edit-question.html', question=question, question_id=question_id)


@app.route("/question/<question_id>/delete", methods=['POST'])
def delete_question(question_id):
    util.handle_deleting_question(question_id)
    return redirect(url_for('route_list'))


@app.route("/answer/<answer_id>/delete", methods=['POST'])
def delete_answer(answer_id):
    #todo jak dostać sie do question id w inny sposob -> jest w templatce html
    question_id = data_manager.get_question_id_by_answer_id(answer_id)['question_id']
    data_manager.delete_comment_by_answer_id(answer_id)
    data_manager.delete_answer(answer_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/question/<question_id>/vote-up", methods=['POST'])
def question_vote_up(question_id):
    data_manager.increase_question_vote_number_count(question_id)
    return redirect(url_for('route_list'))


@app.route("/question/<question_id>/vote-down", methods=['POST'])
def question_vote_down(question_id):
    data_manager.decrease_question_vote_number_count(question_id)
    return redirect(url_for('route_list'))


@app.route("/answer/<answer_id>/vote-up", methods=['POST'])
def answer_vote_up(answer_id):
    question_id = data_manager.get_question_id_by_answer_id(answer_id)['question_id']
    data_manager.increase_answer_vote_number_count(answer_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/answer/<answer_id>/vote-down", methods=['POST'])
def answer_vote_down(answer_id):
    question_id = data_manager.get_question_id_by_answer_id(answer_id)['question_id']
    data_manager.decrease_answer_vote_number_count(answer_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/question/<question_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    #id, message, submission_time, edited_count
    if request.method == 'POST':
        message = request.form.get('message')
        submission_time = data_manager.get_current_time()
        edited_count = 0
        data_manager.add_comment_to_question(question_id, message, submission_time, edited_count)
        return redirect(url_for('display_question', question_id=question_id))
    elif not session.get('username'):
        flash("You need to be logged in to access this page.", 'warning')
        return redirect(url_for('main_page'))
    return render_template('question_comment.html')


@app.route("/answer/<answer_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    question_id = data_manager.get_question_id_by_answer_id(answer_id)['question_id']
    if request.method == 'POST':
        message = request.form.get('message')
        submission_time = data_manager.get_current_time()
        edited_count = 0
        data_manager.add_comment_to_answer(answer_id, message, submission_time, edited_count)
        return redirect(url_for('display_question', question_id=question_id))
    elif not session.get('username'):
        flash("You need to be logged in to access this page.", 'warning')
        return redirect(url_for('main_page'))
    return render_template('answer_comment.html', answer_id=answer_id)


@app.route("/answer/<answer_id>/edit", methods=['POST', 'GET'])
def edit_answer(answer_id):
    question_id = data_manager.get_question_id_by_answer_id(answer_id)['question_id']
    answer = data_manager.get_answer_message_by_id(answer_id)
    if request.method == 'POST':
        data_manager.edit_answer(answer_id, request.form['message'])
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('edit-answer.html', answer=answer, answer_id=answer_id)


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        return validate_login(request.form.get('username'), request.form.get('user-password'))
    elif session.get('username'):
        # session.pop('_flashes', None)
        flash("You are already logged in.", 'warning')
        return redirect(url_for('main_page'))
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        all_usernames = data_manager.get_all_usernames()
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)
        registration_date = data_manager.get_current_time()
        if not any(d['username'] == username for d in all_usernames):
            data_manager.add_user_to_database(username, hashed_password, registration_date)
            return redirect(url_for('main_page'))
        else:
            flash('This username already exist.', 'danger')
    elif session.get('username'):
        flash("You can not access this page, you are already logged in.", 'warning')
        return redirect(url_for('main_page'))
    return render_template('register.html')



@app.route('/logout')
def logout():
    # session.pop('_flashes', None)
    if not session.get('username'):
        flash("You need to be logged in to access this page.", 'warning')
        return redirect(url_for('main_page'))
    session.pop('username', None)
    flash("You have been logged out.", 'success')
    return redirect(url_for('main_page'))


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True)
