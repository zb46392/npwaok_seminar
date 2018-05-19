# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
#from django.http import HttpResponseRedirect
from django.urls import reverse
from forms import UserRegistrationForm, SearchAdsForm, AdDetailsForm, ModifyCategoriesForm
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, authenticate
from .models import Ad, Category, CustomUser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def index(request):
    if request.user.is_authenticated:
        cUser = CustomUser(request.user.id)
        isAdvertiser = cUser.isAdvertiser()
        if request.method == 'POST':
            form = SearchAdsForm(request.POST)
            if form.is_valid():
                if(request.POST.get('searchBtn') != None):
                    category = form.cleaned_data['categories']
                    title = form.cleaned_data['title']
                    priceMin = form.cleaned_data['priceMin']
                    priceMax = form.cleaned_data['priceMax']

                    ads = Ad.findByFilter(category, title, priceMin, priceMax)

                    return render(request, 'oglasnik/index.html',
                        {'form' : form, 'ads':ads,'showTable':True, 'isAdvertiser': isAdvertiser})

                if(request.POST.get("ownAdsBtn") != None):
                    ads = Ad.findByAdvertiser(request.user)
                    return render(request, 'oglasnik/index.html',
                        {'form' : form, 'ads':ads,'showTable':True, 'isAdvertiser': isAdvertiser})

                if(request.POST.get("addAdBtn") != None):
                    return redirect(reverse('newAd'))

        form = SearchAdsForm()


        return render(request, 'oglasnik/index.html',
            {'form' : form, 'showTable': False, 'isAdvertiser': isAdvertiser})

    else:
        return redirect(reverse('login'))

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
    isOwnAd = (request.user == ad.user)

    if request.method == 'POST' and isOwnAd:

        if(request.POST.get('deleteBtn') != None):
            form = AdDetailsForm(initial={
                'title':ad.title, 'description': ad.description,
                'price':ad.price, 'categories': ad.category.pk
                })
            form.fields['title'].disabled = True
            form.fields['description'].disabled = True
            form.fields['price'].disabled = True
            form.fields['categories'].disabled = True
            ad.delete()
            context = {'form': form, 'userData': ad.user.email,'msg': 'Oglas je izbrisan...',
                'isOwnAd': isOwnAd, 'isNewAd': False, 'isDeletedAd': True}

            return render(request, 'oglasnik/adDetails.html', context)

        if(request.POST.get('saveBtn') != None):
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
                context = {'form': form, 'userData': ad.user.email,'msg': 'Oglas upješno pohranjen...',
                    'isOwnAd': isOwnAd, 'isNewAd': False, 'isDeletedAd': False}

                return render(request, 'oglasnik/adDetails.html', context)
    else:
        if(isOwnAd):
            form = AdDetailsForm(initial={
                'title':ad.title, 'description': ad.description,
                'price':ad.price, 'categories': ad.category.pk
                })
            context = {'form': form, 'userData': ad.user.email,'isOwnAd': isOwnAd,
                'isNewAd': False, 'isDeletedAd': False}

            return render(request, 'oglasnik/adDetails.html', context)
        context = {'ad':ad, 'userData': ad.user.email, 'isOwnAd': isOwnAd, 'isNewAd': False,
            'isDeletedAd': False}

        return render(request, 'oglasnik/adDetails.html', context)

@login_required
def createNewAd(request):
    if request.method == 'POST':
        form = AdDetailsForm(request.POST)
        if form.is_valid():
            category = Category.getByName(form.cleaned_data['categories'])
            title = form.cleaned_data['title']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']

            newAd = Ad(category=category, title=title, price=price, description=description,
                user=request.user)
            newAd.save()

        return redirect(reverse('adDetails', args=[newAd.pk]))
    form = AdDetailsForm()
    context = {'form': form, 'userData': request.user.email,'isOwnAd': True, 'isNewAd': True,
        'isDeletedAd': False}
    return render(request, 'oglasnik/adDetails.html', context)


@login_required
def modifyCategories(request):
    isAdmin = False
    if request.user.is_superuser:
        isAdmin = True
        if request.method == 'POST':
            # to_do: create, update, delete Category...
            pass
        else:
            form = ModifyCategoriesForm()
            context = {'form': form, 'isAdmin': isAdmin}
            return render(request, 'oglasnik/modifyCategories.html', context)
    else:
        context = {'isAdmin': isAdmin, 'msg': 'Nemate pravo pristupiti ovoj stranici...'}
        return render(request, 'oglasnik/modifyCategories.html', context)
