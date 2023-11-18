from django.shortcuts import render
from .func import create_db, fill_db, get_marks, get_list_cars, truncate


def index(request):
    marks = get_marks()
    return render(request, 'index.html', {'marks': marks})


def update_autoru_catalog(request):
    create_db()
    truncate()
    fill_db()
    return render(request, 'update.html')


def show_car(request):
    mark = request.GET.get('mark')
    model_lst = get_list_cars(mark)
    return render(request, 'show_car.html', {'model_lst': model_lst})
