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

from .models import Comment
from .models import CommentForm


def coloring_books(request, book_id):
    if request.method == 'POST':
        posted_form = CommentForm(request.POST)
        print('posted_form: ', posted_form)
        if posted_form.is_valid():
            print('posted_form is valid, so save')
            model_instance = posted_form.save(commit=False)
            model_instance.coloring_book_id = book_id
            model_instance.save()
    book = get_coloring_book(book_id)
    form = CommentForm
    comment_list = Comment.objects.filter(
        coloring_book_id=book_id).order_by('-date_added')
    for comment in comment_list:
        comment.stars = get_stars(comment.rating)
    markup = get_likes_markup(request, book['likes'], book_id)
    context = {
        'book': book,
        'form': form,
        'comment_list': comment_list,
        'link_text': markup['link_text'],
        'link_msg': markup['link_msg']
    }
    return render(request, 'coloring_book_view.html', context)

# can remove httpresponse imports if the below isn't needed
# return HttpResponse(


def like(request, book_id):
    num_likes = add_like(book_id)
    response = JsonResponse({
        'num_likes': num_likes
    })
    response.set_cookie(key='likes_coloring_book_'+book_id, value='1')
    return response


def unlike(request, book_id):
    num_likes = subtract_like(book_id)
    response = JsonResponse({
        'num_likes': num_likes
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
