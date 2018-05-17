# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from forms import UserRegistrationForm, SearchAdsForm, AdDetailsForm
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, authenticate
from .models import Ad, Category
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SearchAdsForm(request.POST)
            if form.is_valid():
                category = form.cleaned_data['categories']
                title = form.cleaned_data['title']
                priceMin = form.cleaned_data['priceMin']
                priceMax = form.cleaned_data['priceMax']

                ads = Ad.findByFilter(category, title, priceMin, priceMax)

                return render(request, 'oglasnik/index.html', {'form' : form, 'ads':ads,'visibility':'visible'})
        form = SearchAdsForm()
        return render(request, 'oglasnik/index.html', {'form' : form, 'visibility':'hidden'})

    else:
        return HttpResponseRedirect(reverse('login'))

def registerUser(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
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
        form = UserRegistrationForm()
    return render(request, 'oglasnik/userRegistration.html', {'form': form})

@login_required
def adDetails(request, id):
    ad = Ad.objects.get(pk=id)

    if request.method == 'POST' and request.user == ad.user:
        form = AdDetailsForm(request.POST)
        if form.is_valid():
            category = Category.getByName(form.cleaned_data['categories'])
            title = form.cleaned_data['title']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']

            ad.category = category
            ad.title = title
            ad.price = price
            ad.description = description

            ad.save()
            context = {'form': form, 'userData': ad.user.email,
                'msg': 'Oglas upješno pohranjen...','tableDisplay': 'none'}

            return render(request, 'oglasnik/adDetails.html', context)
    else:
        if(request.user == ad.user):
            form = AdDetailsForm(initial={
                'title':ad.title, 'description': ad.description,
                'price':ad.price, 'categories': ad.category.pk
                })
            context = {'form': form, 'userData': ad.user.email, 'tableDisplay': 'none'}
            return render(request, 'oglasnik/adDetails.html', context)
        context = {'ad':ad, 'userData': ad.user.email, 'formDisplay': 'none' }
        return render(request, 'oglasnik/adDetails.html', context)
