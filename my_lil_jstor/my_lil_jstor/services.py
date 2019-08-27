from django.core.serializers import serialize

from .models import ColoringBook


def get_coloring_book(primary_key):
    coloring_book = ColoringBook.objects.get(pk=primary_key)
    coloring_book_dict = {
        'id': coloring_book.id,
        'title': coloring_book.title,
        'description': coloring_book.description,
        'image_name': coloring_book.image_name,
        'pub_date': coloring_book.pub_date,
        'price': coloring_book.price,
        'likes': coloring_book.likes
    }

    return coloring_book_dict


def add_like(book_id):
    print('add_like: called')
    coloring_book = ColoringBook.objects.get(pk=book_id)
    coloring_book.likes += 1
    coloring_book.save()
    return coloring_book.likes


def subtract_like(book_id):
    print('subtract_like: called')
    coloring_book = ColoringBook.objects.get(pk=book_id)
    coloring_book.likes -= 1
    coloring_book.save()
    return coloring_book.likes


def get_coloring_books_in_range(start, end):
    coloring_books_in_range_list = []
    for i in range(1, end + 1):
        coloring_books_in_range_list.append(get_coloring_book(i))
    return coloring_books_in_range_list


def get_stars(arg):
    if arg is None:
        return ""
    stars = "★" * arg
    return stars


def get_likes_markup(request, num_likes, book_id):
    cookie_name = 'likes_coloring_book_' + book_id
    cookie_val = get_cookie(request, cookie_name)
    link_text = 'Unlike' if cookie_val else 'Like'
    link_msg = 'Be the first to like this'

    if num_likes == 1:
        if cookie_val:
            link_msg = 'You like this'
        else:
            link_msg = '1 person likes this'
    elif num_likes == 2:
        if cookie_val:
            link_msg = 'You and 1 person likes this'
        else:
            link_msg = '2 people like this'
    elif num_likes > 2:
        if cookie_val:
            link_msg = 'You and ' + str(num_likes - 1) + ' people like this'
        else:
            link_msg = str(num_likes) + ' people like this'

    markup = {
        'link_text': link_text,
        'link_msg': link_msg
    }
    print('getLikesMarkup: markup = ', markup)
    return markup


def get_cookie(request, cname):
    print('get_cookie: cname = ', cname)
    # print('get_cookie: request.COOKIES.get(cname) = ', request.COOKIES.get(cname))
    if cname in request.COOKIES:
        return 1
    return 0
