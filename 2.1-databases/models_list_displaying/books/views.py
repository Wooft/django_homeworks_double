from django.core.paginator import Paginator
from django.shortcuts import render

from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'books/books_list.html', context)

def pagi(request, slug):
    content = []
    dates = Book.objects.values_list('pub_date', flat=True)
    for date in dates:
        if date not in content:
            content.append(date)
    pagi = Paginator(content, 1)
    books = Book.objects.filter(pub_date=slug)
    context = {
        'books': books
    }
    return render(request, 'books/books_list.html', context)