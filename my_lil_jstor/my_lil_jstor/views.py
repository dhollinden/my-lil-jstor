from django.http import HttpResponseRedirect
from django.shortcuts import render

from .services import get_coloring_book
from .services import get_coloring_books_in_range
from .models import Comment
from .models import CommentForm


def coloring_books(request, book_id):
    book = get_coloring_book(book_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
        form = CommentForm
        comment_list = Comment.objects.all()
    else:
        form = CommentForm
        comment_list = Comment.objects.all()
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
