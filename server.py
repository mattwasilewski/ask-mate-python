from flask import Flask, render_template, request
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


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True)
