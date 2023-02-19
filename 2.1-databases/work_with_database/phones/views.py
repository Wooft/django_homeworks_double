from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    phones = Phone.objects.all()
    sort = request.GET.get('sort')
    phones = phones.order_by('price')
    if sort == 'name':
        phones = phones.order_by('name')
    if sort == 'min_price':
        phones = phones.order_by('price')
    if sort == 'max_price':
        phones = phones.order_by('-price')
    context = {
        'phones': phones
    }
    return render(request, 'catalog.html', context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.filter(slug=slug)[0]
    context = {
        'phone': phone
    }
    return render(request, 'product.html', context)
