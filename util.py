import data_manager


def get_sorted_questions(sort_method, order):
    if sort_method is None:
        sort_method = 'time'
    if order is None or order == 'desc':
        return sort_questions_by(sort_method, data_manager.get_questions_desc)
    else:
        return sort_questions_by(sort_method, data_manager.get_questions_asc)


def sort_questions_by(sort_method, function):
    match sort_method:
        case 'title':
            return function('title')
        case 'time':
            return function('submission_time')
        case 'message':
            return function('message')
        case 'views':
            return function('view_number')
        case 'votes':
            return function('vote_number')


def handle_deleting_question(question_id):
    answers = data_manager.get_answers_id_by_question_id(question_id)
    for answer_id in answers:
        data_manager.delete_comment_by_answer_id(answer_id['id'])
    data_manager.delete_comment_by_question_id(question_id)
    data_manager.delete_answer_by_question_id(question_id)
    data_manager.delete_question(question_id)