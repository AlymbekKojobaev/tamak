from django import forms
from .models import Order


class ReservationForm(forms.ModelForm):
    '''Форма создание брони унаследована от Orders'''
    class Meta:
        model= Order
        fields = '__all__'
        exclude=['reservator', 'date_created']


