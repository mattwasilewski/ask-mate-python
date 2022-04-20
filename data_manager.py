import csv


def get_all_user_answer():
    file = 'C:\\Users\\lenovo\\Desktop\\workspace\\web\\ask-mate-1-python-mattwasilewski\\answer.csv'

    with open(file) as csvfile:
        my_data = []
        reader = csv.DictReader(csvfile)
        for story in reader:
            new = dict(story)
            my_data.append(new)
        return my_data


def save_file(data_story):
    file = 'C:\\Users\\lenovo\\Desktop\\workspace\\web\\ask-mate-1-python-mattwasilewski\\answer.csv'
    with open(file, "w") as csvfile:
        writer = csv.DictWriter(csvfile)
        writer.writeheader()
        for item in data_story:
            writer.writerow(item)
