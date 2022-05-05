from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import data_manager
import util
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template('main-page.html')


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
    comments = data_manager.get_comment_to_question(question_id)
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_id(question_id)
    return render_template('question.html', answers=answers, question=question,
                           question_id=question_id, comments=comments)


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def new_answer(question_id):
    if request.method == 'POST':
        if 'question-image' in request.files:
            data_manager.save_image_path(request.files['question-image'], request.form.get('message'), question_id)
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
    #todo jak dostać sie do question id w inny sposob -> jest w templatce html
    question_id = data_manager.get_question_id_by_answer_id(answer_id)['question_id']
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


@app.route("/question/<answer_id>/vote-down", methods=['POST'])
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
    return render_template('question_comment.html')


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True)
