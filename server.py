from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import data_manager
import util
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
load_dotenv()
app = Flask(__name__)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        data_manager.set_question_data(request.form['title'], request.form['message'])
        question_id = data_manager.get_last_question()['id']
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add-question.html')


@app.route("/list")
def route_list():
    query_parameters = request.args
    sort_method = query_parameters.get('order_by')
    order = query_parameters.get('order_direction')
    question = util.get_sorted_questions(sort_method, order)
    return render_template('list.html', questions=question)


@app.route("/question/<question_id>")
def display_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_id(question_id)
    return render_template('question.html', answers=answers, question=question,
                           question_id=question_id)


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def new_answer(question_id):
    filename = ''
    if request.method == 'POST':
        if 'question-image' in request.files:
            file = request.files['question-image']
            if file.filename != '' and file and data_manager.allowed_file(file.filename, ALLOWED_EXTENSIONS):
                filename = secure_filename(file.filename)
                file.save(os.path.join(BASE_PATH + UPLOAD_FOLDER, filename))
        submission_time = data_manager.get_current_time()
        vote_number = '0'
        message = request.form.get('message')
        #todo bug ze zdjeciem
        image = UPLOAD_FOLDER + '/' + filename
        data_manager.add_answer(submission_time, vote_number, question_id, message, image)
        return redirect(url_for('display_question', question_id=question_id))
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
    data_manager.delete_question(question_id)
    return redirect(url_for('route_list'))


@app.route("/answer/<answer_id>/delete", methods=['POST'])
def delete_answer(answer_id):
    question_id = data_manager.get_question_id_by_answer_id(answer_id)['question_id']
    data_manager.delete_answer(answer_id)
    return redirect(url_for('display_question', question_id=question_id))


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True)
