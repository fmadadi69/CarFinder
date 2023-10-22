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


def predict_price(car):
    x, y = [], []
    make, year, mileage, location = [], [], [], []

    all_cars = Car.objects.all()
    for car in all_cars:
        make.append([car.make])
        year.append([car.year])
        mileage.append([car.mileage])
        location.append([car.location])
        # x.append([car.make, car.year, car.mileage, car.location])
        y.append(car.price)

    # clf = tree.DecisionTreeClassifier()
    # clf = clf.fit(x, y)
    # return clf.predict([car])
    encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
    encoder.fit(make)
    encoded_make = encoder.transform(make)
    encoder.fit(year)
    encoded_year = encoder.transform(make)
    encoder.fit(mileage)
    encoded_mileage = encoder.transform(make)
    encoder.fit(location)
    encoded_location = encoder.transform(make)
    encoded_zip = []
    for make_z, year_z, mileage_z, location_z in zip(encoded_make, encoded_year, encoded_mileage, encoded_location):
        encoded_zip.append([make_z, year_z, mileage_z, location_z])

    x_train, x_test, y_train, y_test = train_test_split(encoded_zip, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    mse = mean_squared_error(y_test, predictions)
    print(f'mean squared error: {mse}')
    return predictions


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
