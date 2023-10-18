from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def car_predict(request):
    return HttpResponse('مشخصات خوردروی مورد نظرتان را وارد کنید تا قیمت آن را تخمین بزنیم:')


def similar_cars(request , prediction_id):
    return HttpResponse('لیست خودروهای مشابه مورد نظر شما')


def cars_list(request):
    return HttpResponse('لیست کلیه خودرو ها')

