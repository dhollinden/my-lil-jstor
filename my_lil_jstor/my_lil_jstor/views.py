from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from .services import get_coloring_book
from .services import get_coloring_books_in_range
from .services import get_stars
from .services import add_like
from .services import subtract_like
from .services import get_likes_markup
from .services import get_discounted_price


from .models import Comment
from .models import CommentForm

from decimal import Decimal, ROUND_UP


def coloring_books(request, book_id):
    if request.method == 'POST':
        posted_form = CommentForm(request.POST)
        if posted_form.is_valid():
            model_instance = posted_form.save(commit=False)
            model_instance.coloring_book_id = book_id
            model_instance.save()
    book = get_coloring_book(book_id)
    form = CommentForm
    comment_list = Comment.objects.filter(
        coloring_book_id=book_id).order_by('-date_added')
    total = 0
    count = 0
    for comment in comment_list:
        comment.stars = get_stars(comment.rating)
        print('coloring_book view: comment.rating = ', comment.rating)
        if comment.rating:
            count += 1
            total += int(comment.rating)
            comment.non_stars = get_stars(5 - comment.rating)
        else:
            comment.non_stars = ""
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

    markup = get_likes_markup(request, book['likes'], book_id)
    discounted_price = get_discounted_price(book_id)
    if discounted_price < 2.50:
        discounted_price = round(Decimal(2.50), 2)
    context = {
        'book': book,
        'discounted_price': discounted_price,
        'form': form,
        'comment_average_text': comment_average_text,
        'comment_average_stars': comment_average_stars,
        'comment_average_stars_alt': comment_average_stars_alt,
        'comment_list': comment_list,
        'comment_header': comment_header,
        'leave_comment_header': leave_comment_header,
        'link_text': markup['link_text'],
        'link_msg': markup['link_msg']
    }
    return render(request, 'coloring_book_view.html', context)

# can remove httpresponse imports if the below isn't needed
# return HttpResponse(


def like(request, book_id):
    num_likes = add_like(book_id)
    discounted_price = get_discounted_price(book_id)
    response = JsonResponse({
        'num_likes': num_likes,
        'discounted_price': discounted_price
    })
    response.set_cookie(key='likes_coloring_book_'+book_id, value='1')
    return response


def unlike(request, book_id):
    num_likes = subtract_like(book_id)
    discounted_price = get_discounted_price(book_id)
    response = JsonResponse({
        'num_likes': num_likes,
        'discounted_price': discounted_price
    })
    response.delete_cookie('likes_coloring_book_' + book_id)
    return response


def browse(request):
    books_list = get_coloring_books_in_range(1, 5)
    context = {
        'books_list': books_list
    }
    return render(request, 'browse.html', context)


def home(request):
    book = get_coloring_book(3)
    context = {
        'book': book
    }
    return render(request, 'home.html', context)


def purchase(request, book_id):
    book = get_coloring_book(book_id)
    context = {
        'book': book
    }
    return render(request, 'purchase.html', context)
