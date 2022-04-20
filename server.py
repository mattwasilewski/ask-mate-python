from flask import Flask, render_template, request, redirect
import data_manager
import util

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/list", methods=['GET', 'POST'])
def route_list():
    questions = data_manager.convert_data('sample_data/question.csv')
    if request.method == 'POST':
        sort_method = request.form['sort']
        order = request.form['order']
        questions = util.get_sorted_items(questions, sort_method, order)
    else:
        query_parameters = request.args
        sort_method = query_parameters.get('order_by')
        order = query_parameters.get('order_direction')
        questions = util.get_sorted_items(questions, sort_method, order)
    return render_template('list.html', questions=questions)


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def new_answer(question_id):
    answer = {}
    answers = data_manager.convert_data('sample_data/answer.csv')
    current_time = data_manager.get_timestamp()
    if request.method == 'POST':
        answer['id'] = len(answers) + 1
        answer['submission_time'] = current_time[int(question_id)]
        answer['vote_number'] = '0'
        answer['question_id'] = question_id
        answer['message'] = request.form['message']
        answer['image'] = 'img.url'
        data_manager.save_file(answer)
        return redirect('/list')
    return render_template('question.html', question_id=question_id)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True)
