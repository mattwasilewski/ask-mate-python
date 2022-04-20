from connection import ANSWER_DATA_FILE_PATH, QUESTION_DATA_FILE_PATH
import connection
from datetime import datetime
import csv
QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_data():
    answer_data = connection.get_data('sample_data/answer.csv')
    question_data = connection.get_data('sample_data/question.csv')
    return answer_data, question_data


def get_all_answers():
    file = 'sample_data/answer.csv'
    with open(file) as csvfile:
        my_data = []
        reader = csv.DictReader(csvfile)
        for story in reader:
            new = dict(story)
            my_data.append(new)
        return my_data


def save_file(new_answer):
    data_file = open('sample_data/answer.csv', 'a', newline='')
    fieldnames = connection.ANSWER_HEADERS
    writer = csv.DictWriter(data_file, fieldnames=fieldnames)
    writer.writerow(new_answer)


def get_timestamp():
    answer, question = get_all_data()
    timestamps = [int(row['submission_time']) for row in question]
    return timestamps


def timestamp_to_datetime():
    dates = []
    timestamps = get_timestamp()
    for timestamp in timestamps:
        value = datetime.utcfromtimestamp(timestamp)
        dates.append(f"{value:%Y-%m-%d %H:%M:%S}")
    return dates
