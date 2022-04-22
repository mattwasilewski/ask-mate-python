from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import data_manager
import util
import os

app = Flask(__name__)


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
    new_answers = None
    questions = data_manager.convert_data(data_manager.QUESTION_DATA_FILE_PATH)
    answers = data_manager.convert_data(data_manager.ANSWER_DATA_FILE_PATH)
    return render_template('question.html', answers=answers, questions=questions,
                           question_id=question_id, new_answer=new_answers)


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def new_answer(question_id):
    answer = {}
    answers = data_manager.get_data(data_manager.ANSWER_DATA_FILE_PATH)
    answer_count = 1
    for answer in answers:
        if answer['question_id'] == question_id:
            answer_count += 1
    if request.method == 'POST':
        answer['id'] = answer_count
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
    questions = data_manager.convert_data(data_manager.QUESTION_DATA_FILE_PATH)
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


@app.route("/update/<question_id>", methods=['POST', 'GET'])
def upload_image(question_id):
    app_root = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(app_root, 'static/')
    for upload in request.files.getlist("file"):
        filename = upload.filename
        destination = "/".join([target, filename])
        upload.save(destination)
    return render_template("question.html", image_name=filename, question_id=question_id)


'''@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory('static', filename)'''


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True)
