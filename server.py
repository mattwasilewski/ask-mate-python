
from flask import Flask, render_template, request, redirect
import data_manager

app = Flask(__name__)


@app.route("/list", methods=['POST', 'GET'])
def route_list():
    date = data_manager.timestamp_to_datetime()
    answers, questions = data_manager.get_all_data()
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
    answer_count = 1
    for answer in answers:
        if answer['question_id'] == question_id:
            answer_count += 1
    if request.method == 'POST':
        answer['id'] = answer_count
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
        debug=True)
