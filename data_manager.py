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


def save_new_answer(new_answer):
    data_file = open(ANSWER_DATA_FILE_PATH, 'a', newline='')
    fieldnames = ANSWER_HEADERS
    writer = csv.DictWriter(data_file, fieldnames=fieldnames)
    writer.writerow(new_answer)


def save_updated_data(updated_data):
    csvfile = open(QUESTION_DATA_FILE_PATH, 'w', newline='')
    fieldnames = QUESTION_HEADERS
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for story in updated_data:
        writer.writerow(story)


def get_current_time():
    current_time = int(datetime.now().timestamp())
    return current_time

