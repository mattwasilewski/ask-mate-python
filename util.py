import data_manager


def get_sorted_questions(sort_method, order):
    if sort_method is None:
        sort_method = 'time'
    if order is None or order == 'desc':
        return sort_questions_by(sort_method, data_manager.get_questions_desc)
    else:
        return sort_questions_by(sort_method, data_manager.get_questions_asc)


def sort_questions_by(sort_method, function):
    # questions = convert_questions()
    match sort_method:
        case 'title':
            # return sorted(questions, key=lambda item: item['title'], reverse=order)
            return function('title')
        case 'time':
            return function('submission_time')
            # return sorted(questions, key=lambda item: item['submission_time'], reverse=order)
        case 'message':
            return function('message')
            # return sorted(questions, key=lambda item: item['message'], reverse=order)
        case 'views':
            return function('view_number')
            # return sorted(questions, key=lambda item: int(item['view_number']), reverse=order)
        case 'votes':
            return function('vote_number')
            # return sorted(questions, key=lambda item: int(item['vote_number']), reverse=order)

