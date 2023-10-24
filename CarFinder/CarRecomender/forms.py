from django import forms
from .models import CarPrediction, Car
from django.utils.translation import gettext_lazy as _


class CarPredictionForm(forms.ModelForm):
    make = forms.ModelChoiceField(queryset=Car.objects.values_list('make', flat=True).distinct(),
                                  empty_label=None, to_field_name="make", label='مدل')

    class Meta:
        model = CarPrediction
        fields = ['make', 'year', 'mileage', 'location']
        labels = {
            'make': _("مدل"),
            'year': _("سال ساخت"),
            'mileage': _("کارکرد"),
            'location': _("مکان"),
        }
