from flask import Flask, render_template, request, redirect, url_for
import data_manager
import util

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/list", methods=['GET', 'POST'])
def route_list():
    questions = data_manager.convert_data(data_manager.QUESTION_DATA_FILE_PATH)
    if request.method == 'POST':
        sort_method = request.form['sort_by']
        order = request.form['order_direction']
        questions = util.get_sorted_items(questions, sort_method, order)
    else:
        query_parameters = request.args
        sort_method = query_parameters.get('order_by')
        order = query_parameters.get('order_direction')
        questions = util.get_sorted_items(questions, sort_method, order)
    return render_template('list.html', questions=questions)


@app.route("/question/<question_id>")
def display_question(question_id):
    new_answer = None
    questions = data_manager.convert_data(data_manager.QUESTION_DATA_FILE_PATH)
    answers = data_manager.convert_data(data_manager.ANSWER_DATA_FILE_PATH)
    return render_template('question.html', answers=answers, questions=questions,
                           question_id=question_id, new_answer=new_answer)


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def new_answer(question_id):
    answer = {}
    answers = data_manager.convert_data(data_manager.ANSWER_DATA_FILE_PATH)
    if request.method == 'POST':
        answer['id'] = len(answers) + 1
        answer['submission_time'] = data_manager.get_current_time()
        answer['vote_number'] = '0'
        answer['question_id'] = question_id
        answer['message'] = request.form['message']
        answer['image'] = 'img.url'
        data_manager.save_new_answer(answer)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('question.html', question_id=question_id)


@app.route("/question/<question_id>/edit", methods=['POST', 'GET'])
def edit_question(question_id):
    questions = data_manager.get_data(data_manager.QUESTION_DATA_FILE_PATH)
    if request.method == 'POST':
        updated_data = []
        for row in questions:
            for key, value in row.items():
                if key == 'id' and value == question_id:
                    row['title'] = request.form['title']
                    row['message'] = request.form['message']
                    row['submission_time'] = data_manager.get_current_time()
            updated_data.append(row)
            data_manager.save_updated_data(updated_data)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('edit_question.html', questions=questions, question_id=question_id)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True)
