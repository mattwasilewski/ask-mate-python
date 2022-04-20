
from flask import Flask, render_template, request, redirect
import data_manager

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/list", methods=['GET', 'POST'])
def route_list():
    date = data_manager.timestamp_to_datetime()
    answers, questions = data_manager.get_all_data()
    questions = sorted(questions, key=lambda item: item['submission_time'])
    if request.method == "POST":
        sort_option = request.form['sort']
        order = request.form['order']

    return render_template('list.html', questions=questions, date=date)



    # if wybrany z options rodzaj sortowania
    # return list html z wybranym rodzajem sortowania w jako klucz słownika
    # np. sorted(questions, key=lambda item: item['view_number'], reverse=True)
    return render_template('list.html',
                           questions=sorted(questions, key=lambda item: item['submission_time']),
                           date=date)


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def new_answer(question_id):
    answer = {}
    answers = data_manager.get_all_answers()
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
