from flask import Flask, render_template, request, redirect, url_for
import data_manager
import util

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/list")
def route_list():
    #todo pojedyncza zmienic iteracje w pliku list.html na iteracje w pythonie - o ile się da?
    query_parameters = request.args
    sort_method = query_parameters.get('order_by')
    order = query_parameters.get('order_direction')
    sorted_questions = util.get_sorted_items(sort_method, order)
    return render_template('list.html', sorted_questions=sorted_questions)


@app.route("/question/<question_id>")
def display_question(question_id):
    new_answer = None
    question = data_manager.get_converted_question(question_id)
    answers = data_manager.get_converted_answers(question_id)
    return render_template('question.html', answers=answers, question=question,
                           question_id=question_id, new_answer=new_answer)


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def new_answer(question_id):
    if request.method == 'POST':
        print('siema')
        data_manager.add_answer(question_id, request.form['message'])
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('question.html', question_id=question_id)


@app.route("/question/<question_id>/edit", methods=['POST', 'GET'])
def edit_question(question_id):
    question = data_manager.get_question(question_id)
    if request.method == 'POST':
        data_manager.update_question(question_id, request.form['title'], request.form['message'])
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('edit_question.html', question=question, question_id=question_id)


@app.route("/question/<question_id>/delete", methods=['POST'])
def delete_question(question_id):
    print('test')
    return redirect(url_for('display_question', question_id=question_id))


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True)
