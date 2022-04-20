import csv
import os


# functions to read, write, appends CSV files
QUESTION_DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
ANSWER_DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'answer.csv'
QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_data(data_file):
    csvfile = open(data_file)
    dictionaries = csv.DictReader(csvfile)
    return dictionaries



# DODAWAC NOWE PYTANIE NA POCZĄTEK LISTY

# def save_new_question(new_question=None):
#     csvfile = open(QUESTION_DATA_FILE_PATH, 'a', newline='')
#     fieldnames = QUESTION_HEADERS