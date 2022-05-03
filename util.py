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

