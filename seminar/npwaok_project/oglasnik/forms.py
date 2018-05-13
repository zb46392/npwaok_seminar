# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class userRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True,
        label='Email adresa', help_text='Obavezno.')

    CHOICES = [('user','Korisnik'), ('advertiser','Oglašivač')]
    choice = forms.ChoiceField(choices=CHOICES, label='Registriraj se kao',
        widget=forms.RadioSelect(), initial='user')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'choice',)
