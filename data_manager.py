from connection import ANSWER_DATA_FILE_PATH, QUESTION_DATA_FILE_PATH
import connection
from datetime import datetime


def get_all_data():
    answer_data = connection.get_data(ANSWER_DATA_FILE_PATH)
    question_data = connection.get_data('sample_data/question.csv')
    return answer_data, question_data


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
