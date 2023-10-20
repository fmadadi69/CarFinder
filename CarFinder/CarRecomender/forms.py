from django import forms
from .models import CarPrediction
from django.utils.translation import gettext_lazy as _


class CarPredictionForm(forms.ModelForm):
    class Meta:
        model = CarPrediction
        fields = ['make', 'year', 'mileage', 'location']
        labels = {
            'make': _("مدل"),
            'year': _("سال ساخت"),
            'mileage': _("کارکرد"),
            'location': _("مکان"),
        }
