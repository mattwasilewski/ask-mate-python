from flask import Flask, render_template
import data_manager

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/list")
def route_list():
    date = data_manager.timestamp_to_datetime()
    answers, questions = data_manager.get_all_data()
    return render_template('list.html', questions=questions, date=date)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True)
