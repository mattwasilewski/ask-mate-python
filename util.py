def get_sorted_items(items, sort_method, order):
    if order is None:
        order = 'desc'
    if sort_method is None:
        sort_method = 'time'
    order = True if order == 'desc' else False
    return sort_items_by(items, sort_method, order)


def sort_items_by(items, sort_method, order):
    match sort_method:
        case 'title':
            return sorted(items, key=lambda item: item['title'], reverse=order)
        case 'time':
            return sorted(items, key=lambda item: item['submission_time'], reverse=order)
        case 'message':
            return sorted(items, key=lambda item: item['message'], reverse=order)
        case 'views':
            return sorted(items, key=lambda item: int(item['view_number']), reverse=order)
        case 'votes':
            return sorted(items, key=lambda item: int(item['vote_number']), reverse=order)
