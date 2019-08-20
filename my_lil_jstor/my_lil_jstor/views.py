from django.http import HttpResponseRedirect
from django.shortcuts import render

from .services import get_coloring_book
from .services import get_coloring_books_in_range
from .services import get_stars
from .models import Comment
from .models import CommentForm


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
    for comment in comment_list:
        comment.stars = get_stars(comment.rating)
    context = {
        'book': book,
        'form': form,
        'comment_list': comment_list
    }
    return render(request, 'coloring_book_view.html', context)


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
