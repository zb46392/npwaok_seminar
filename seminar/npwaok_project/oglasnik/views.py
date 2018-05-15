# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from forms import userRegistrationForm, searchAdsForm
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, authenticate
from .models import Ad
from django.http import HttpResponse

def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = searchAdsForm(request.POST)
            if form.is_valid():
                category = form.cleaned_data['categories']
                title = form.cleaned_data['title']
                priceMin = form.cleaned_data['priceMin']
                priceMax = form.cleaned_data['priceMax']

                ads = Ad.findByFilter(category, title, priceMin, priceMax)

                return render(request, 'oglasnik/index.html', {'form' : form, 'ads':ads,'visibility':'visible'})
        form = searchAdsForm()
        return render(request, 'oglasnik/index.html', {'form' : form, 'visibility':'hidden'})

    else:
        return HttpResponseRedirect(reverse('login'))

def registerUser(request):
    if request.method == 'POST':
        form = userRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'])
            if form.cleaned_data['choice'] == 'advertiser':
                advertisersGrp = Group.objects.get(name='Advertisers')
                advertisersGrp.user_set.add(user)
                advertisersGrp.save()


            login(request,user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = userRegistrationForm()
    return render(request, 'oglasnik/userRegistration.html', {'form': form})


def adDetails(request, id):
    if request.method == 'POST':
        pass
    else:
        ad = Ad.objects.get(pk=id)

        context = {'ad':ad, 'userData': ad.user.email }
        return render(request, 'oglasnik/adDetails.html', context)
