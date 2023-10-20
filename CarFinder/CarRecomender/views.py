from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.utils import timezone

from .models import Car, CarPrediction
from .forms import CarPredictionForm


# Create your views here.
def car_prediction(request):
    if request.method == 'POST':
        form = CarPredictionForm(request.POST)
        if form.is_valid():
            car_prediction_form = form.save(commit=False)
            car_prediction_form.predicted_price = 100 #WRITE A FUNCTION TO PREDICT PRICE
            car_prediction_form.prediction_date = timezone.now()
            car_prediction_form.save()

            return redirect(reverse('similar_cars', kwargs={'prediction_id': car_prediction_form.id}))
        else:
            return HttpResponse("Form is not valid. Please check your input.")
    else:
        form = CarPredictionForm()
    return render(request, 'CarRecomender/CarPrediction.html', {'form': form})


def similar_cars(request, prediction_id):
    prediction = get_object_or_404(CarPrediction, pk=prediction_id)
    form = CarPredictionForm(initial={
        'make': prediction.make,
        'mileage': prediction.mileage,
        'year': prediction.year,
        'location': prediction.location
    })
    similar_cars = get_list_or_404(Car) #ADD FILTER QUERY TO SHOW ONLY SIMILAR CARS
    return render(request, 'CarRecomender/SimilarCar.html',
                  {'form': form, 'prediction': prediction, 'similar_cars': similar_cars})


def cars_list(request):
    return HttpResponse('لیست کلیه خودرو ها')
