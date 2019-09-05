from django.core.serializers import serialize
from decimal import Decimal, ROUND_DOWN
from .models import ColoringBook, Comment


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


def update_likes(book_id, action):
    coloring_book = ColoringBook.objects.get(pk=book_id)
    if action == 'like':
        coloring_book.likes += 1
    else:
        coloring_book.likes -= 1
    coloring_book.save()
    return coloring_book.likes


def get_discounted_price(book_id):
    coloring_book_dict = get_coloring_book(book_id)
    num_likes = coloring_book_dict['likes']
    num_comments = len(Comment.objects.filter(coloring_book_id=book_id))
    price = coloring_book_dict['price']
    minimum_price = 2.50
    discounted_price = price - Decimal(num_likes * .25 + num_comments * .5)
    if discounted_price < minimum_price:
        discounted_price = Decimal(str(minimum_price)).quantize(
            Decimal('.01'), rounding=ROUND_DOWN)
    return discounted_price


def get_coloring_books_in_range(start, end):
    coloring_books_in_range_list = []
    for i in range(start, end + 1):
        coloring_books_in_range_list.append(get_coloring_book(i))
    return coloring_books_in_range_list


def get_stars(arg):
    if arg is None:
        return ""
    star = "★"
    stars = star * arg
    return stars


def get_comment_markup(book_id):
    comment_list = Comment.objects.filter(
        coloring_book_id=book_id).order_by('-date_added')
    total = 0
    count = 0
    for comment in comment_list:
        comment.stars = get_stars(comment.rating)
        comment.non_stars = ""
        if comment.rating:
            count += 1
            total += int(comment.rating)
            comment.non_stars = get_stars(5 - comment.rating)
    if count > 0:
        comment_average = round(total / count, 1)
        comment_average_int = int((1.0*total/count) + 0.5)
        comment_average_text = str(comment_average) + ' out of 5 stars'
        comment_average_stars = get_stars(comment_average_int)
        comment_average_stars_alt = get_stars(int(5) - comment_average_int)
    else:
        comment_average_text = "Not yet rated"
        comment_average_stars = ""
        comment_average_stars_alt = ""
    num_comments = len(comment_list)
    if num_comments == 0:
        comment_header = ''
        leave_comment_header = 'Be the first to comment!'
    elif num_comments == 1:
        comment_header = '1 Customer Comment'
        leave_comment_header = 'Leave a comment'
    else:
        comment_header = str(num_comments) + ' Customer Comments'
        leave_comment_header = 'Leave a comment'

    comment_markup = {
        'comment_list': comment_list,
        'comment_average_text': comment_average_text,
        'comment_average_stars': comment_average_stars,
        'comment_average_stars_alt': comment_average_stars_alt,
        'comment_header': comment_header,
        'leave_comment_header': leave_comment_header
    }

    return comment_markup


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

    likes_markup = {
        'link_text': link_text,
        'link_msg': link_msg
    }

    return likes_markup


def get_cookie(request, cname):
    # print('get_cookie: request.COOKIES.get(cname) = ', request.COOKIES.get(cname))
    if cname in request.COOKIES:
        return 1
    return 0
