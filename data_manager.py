from flask import request
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


def add_answer(question_id):
    answers = convert_data(ANSWER_DATA_FILE_PATH)
    answer = {}
    answer['id'] = len(answers) + 1
    answer['submission_time'] = get_current_time()
    answer['vote_number'] = '0'
    answer['question_id'] = question_id
    answer['message'] = request.form['message']
    answer['image'] = 'img.url'
    save_new_answer(answer)


def update_data(question_id, questions):
    updated_data = []
    for row in questions:
        for key, value in row.items():
            if key == 'id' and value == question_id:
                row['title'] = request.form['title']
                row['message'] = request.form['message']
                row['submission_time'] = get_current_time()
        updated_data.append(row)
        save_updated_data(updated_data)