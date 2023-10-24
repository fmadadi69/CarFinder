from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

from .models import Car, CarPrediction
from .forms import CarPredictionForm
import pandas as pd
import numpy as np


def predict_price(user_car):
    # ############### Creating Train set ################ #
    data, x, y = [], [], []
    all_cars = Car.objects.all()
    for car in all_cars:
        data.append([car.make, car.year, car.mileage, car.location, car.price])

    df = pd.DataFrame(data, columns=['make', 'year', 'mileage', 'location', 'price'])
    encoder = OneHotEncoder(sparse=False)
    df_encoded = encoder.fit_transform(df[['make', 'location']])
    df_encoded_df = pd.DataFrame(df_encoded, columns=encoder.get_feature_names_out(['make', 'location']))
    df = pd.concat([df, df_encoded_df], axis=1)
    df = df.drop(['make', 'location'], axis=1)
    x = df.drop('price', axis=1)
    y = df['price']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(x, y)

    # ################ Creating Test set ################# #
    car_df = pd.DataFrame([user_car], columns=['make', 'year', 'mileage', 'location'])
    car_encoded = encoder.transform(car_df[['make', 'location']])
    car_encoded_df = pd.DataFrame(car_encoded, columns=encoder.get_feature_names_out(['make', 'location']))
    car_df = pd.concat([car_df, car_encoded_df], axis=1)
    car_df = car_df.drop(['make', 'location'], axis=1)

    predicted_price = model.predict(car_df)
    predicted_price_int = np.round(predicted_price).astype(int)

    return predicted_price_int[0]


# Create your views here.
def car_prediction(request):
    if request.method == 'POST':
        form = CarPredictionForm(request.POST)
        if form.is_valid():
            user_desired_car = [
                form.cleaned_data['make'],
                form.cleaned_data['year'],
                form.cleaned_data['mileage'],
                form.cleaned_data['location']
            ]
            car_prediction_form = form.save(commit=False)
            car_prediction_form.predicted_price = predict_price(user_desired_car)
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
    all_similar_cars = get_list_or_404(Car)  # ADD FILTER QUERY TO SHOW ONLY SIMILAR CARS
    return render(request, 'CarRecomender/SimilarCar.html',
                  {'form': form, 'prediction': prediction, 'similar_cars': all_similar_cars})


class CarsListView(generic.ListView):
    template_name = 'CarRecomender/CarsList.html'
    context_object_name = 'cars_list'

    def get_queryset(self):
        return Car.objects.all()
