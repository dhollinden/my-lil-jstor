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
        'price': coloring_book.price
    }

    return coloring_book_dict


def get_coloring_books_in_range(start, end):
    coloring_books_in_range_list = []
    for i in range(1, end + 1):
        coloring_books_in_range_list.append(get_coloring_book(i))
    return coloring_books_in_range_list
