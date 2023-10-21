from django.urls import path

from . import views

urlpatterns = [
    path("car_prediction/", views.car_prediction, name='car_prediction'),
    path("<int:prediction_id>/similar_cars/", views.similar_cars, name='similar_cars'),
    path("cars_list/", views.CarsListView.as_view(), name='cars_list')
]
