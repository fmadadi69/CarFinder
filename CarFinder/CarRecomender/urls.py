from django.urls import path

from . import views

urlpatterns = [
    path("car_predict/", views.car_predict, name='car_predict'),
    path("<int:prediction_id>/similar_cars/", views.similar_cars, name='similar_cars'),
    path("cars_list/", views.cars_list, name='cars_list')
]
