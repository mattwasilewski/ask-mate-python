from flask import Flask, render_template, request
import data_manager

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/list")
def route_list():
    date = data_manager.timestamp_to_datetime()
    answers, questions = data_manager.get_all_data()
    # if wybrany z options rodzaj sortowania
    # return list html z wybranym rodzajem sortowania w jako klucz słownika
    # np. sorted(questions, key=lambda item: item['view_number'], reverse=True)
    return render_template('list.html',
                           questions=sorted(questions, key=lambda item: item['submission_time']),
                           date=date)



if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True)
