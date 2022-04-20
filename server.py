from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import data_manager

app = Flask(__name__)


@app.route("/question/1", methods=['POST', 'GET'])
def new_answer():
    all_answers = data_manager.get_all_user_answer()
    answer = {}
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if request.method == 'POST':
        answer['id'] = len(all_answers)
        answer['submission_time'] = current_time
        answer['vote_number'] = '0'
        answer['question_id'] = '1'
        answer['message'] = request.form['message']
        answer['image'] = 'img.url'
        all_answers.append(answer)
        data_manager.save_file(all_answers)
        return redirect('/')
    return render_template('question.html')





if __name__ == '__main__':
    app.run(
        debug=True
    )