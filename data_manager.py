import os
from datetime import datetime
import csv

QUESTION_DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
ANSWER_DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'answer.csv'
QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_data(datafile):
    with open(datafile) as csvfile:
        reader = csv.DictReader(csvfile)
        items = [dict(story) for story in reader]
        return items


def convert_data(datafile):
    converted_data = get_data(datafile)
    for row in converted_data:
        value = datetime.utcfromtimestamp(int(row['submission_time']))
        row['submission_time'] = f"{value:%Y-%m-%d %H:%M:%S}"
    return converted_data


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
    fieldnames = ANSWER_HEADERS
    writer = csv.DictWriter(data_file, fieldnames=fieldnames)
    writer.writerow(new_answer)


def get_current_time():
    current_time = int(datetime.now().timestamp())
    return current_time


# do wywalenia
def get_timestamp():
    questions = convert_data('sample_data/question.csv')
    timestamps = [row['submission_time'] for row in questions]
    return timestamps
