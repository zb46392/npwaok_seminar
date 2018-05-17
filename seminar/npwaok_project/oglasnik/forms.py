# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from models import Category


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True,
        label='Email adresa', help_text='Obavezno.')

    CHOICES = [('user','Korisnik'), ('advertiser','Oglašivač')]
    choice = forms.ChoiceField(choices=CHOICES, label='Registriraj se kao',
        widget=forms.RadioSelect(), initial='user')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'choice',)

class SearchAdsForm(forms.Form):
    categories = forms.ModelChoiceField(queryset=Category.getAll(),
        empty_label="(Sve)", required=False)
    title = forms.CharField(max_length = 40, label = 'Traži pojam',
        required=False)
    priceMin = forms.DecimalField(max_digits = 8, decimal_places = 2,
        label='Minimalna cjena', min_value=0, required=False)
    priceMax = forms.DecimalField(max_digits = 8, decimal_places = 2,
        label='Maximalna cjena',  min_value=0, required=False)

class AdDetailsForm(forms.Form):
    categories = forms.ModelChoiceField(queryset=Category.getAll(),
        label = "Kategorija", required=True)
    title = forms.CharField(max_length = 40,label = 'Naslov', required=False)
    price = forms.DecimalField(max_digits = 8, label= 'Cijena',decimal_places = 2,
        min_value=0, required=False)
    description = forms.CharField(widget=forms.Textarea, label = 'Opis')
