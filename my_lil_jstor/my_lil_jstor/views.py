from django.http import JsonResponse
from django.shortcuts import render

from .services import *

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
    comment_markup = get_comment_markup(book_id)
    likes_markup = get_likes_markup(request, book['likes'], book_id)
    discounted_price = get_discounted_price(book_id)
    form = CommentForm
    if discounted_price < 2.50:
        discounted_price = round(Decimal(2.50), 2)
    context = {
        'book': book,
        'comment_markup': comment_markup,
        'likes_markup': likes_markup,
        'discounted_price': discounted_price,
        'form': form
    }
    return render(request, 'coloring_book_view.html', context)


def likes_handler(request, book_id, action):
    num_likes = update_likes(book_id, action)
    discounted_price = get_discounted_price(book_id)
    response = JsonResponse({
        'num_likes': num_likes,
        'discounted_price': discounted_price
    })
    if action == 'like':
        response.set_cookie(key='likes_coloring_book_'+book_id, value='1')
    else:
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
