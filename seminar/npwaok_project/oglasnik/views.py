# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
#from django.http import HttpResponseRedirect
from django.urls import reverse
from forms import (UserRegistrationForm, SearchAdsForm, AdDetailsForm,
    ModifyCategoriesForm, ImageForm)
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, authenticate
from .models import Ad, Category, CustomUser, AdsImages
from django.contrib.auth.decorators import login_required
#from django.core.files.storage import FileSystemStorage
#from decimal import Decimal
from django.conf import settings
import os
#from django.http import HttpResponse

ADVERTISERS_ROOT = settings.MEDIA_ROOT + '/advertisers/'

def index(request):
    if request.user.is_authenticated:
        cUser = CustomUser(request.user.id)
        isAdvertiser = cUser.isAdvertiser()
        isAdmin = request.user.is_superuser
        if request.method == 'POST':
            form = SearchAdsForm(request.POST)
            if form.is_valid():
                if(request.POST.get('searchBtn') != None):
                    category = form.cleaned_data['categories']
                    title = form.cleaned_data['title']
                    priceMin = form.cleaned_data['priceMin']
                    priceMax = form.cleaned_data['priceMax']

                    query = {'category': str(category), 'title': title,
                        'priceMin': str(priceMin), 'priceMax': str(priceMax)}

                    request.session['query'] = query
                    request.session['ownAds'] = False

                    ads = Ad.findByFilter(category, title, priceMin, priceMax)

                    return render(request, 'oglasnik/index.html',
                        {'form' : form, 'ads':ads,'showTable':True,
                            'isAdvertiser': isAdvertiser, 'isAdmin': isAdmin})

                if(request.POST.get("ownAdsBtn") != None):
                    ads = Ad.findByAdvertiser(request.user)

                    request.session['query'] = None
                    request.session['ownAds'] = True

                    return render(request, 'oglasnik/index.html',
                        {'form' : form, 'ads':ads,'showTable':True,
                            'isAdvertiser': isAdvertiser, 'isAdmin': isAdmin})

                if(request.POST.get("addAdBtn") != None):
                    return redirect(reverse('newAd'))

        form = SearchAdsForm()
        if request.session.get('query', None) != None:
            category = Category.getByName(request.session['query']['category'])
            title = request.session['query']['title']
            if request.session['query']['priceMin'] == 'None':
                priceMin = None
            else:
                priceMin = request.session['query']['priceMin']

            if request.session['query']['priceMax'] == 'None':
                priceMax = None
            else:
                priceMax = request.session['query']['priceMax']
            ads = Ad.findByFilter(category, title, priceMin, priceMax)

            return render(request, 'oglasnik/index.html',
                {'form' : form, 'showTable': True, 'isAdvertiser': isAdvertiser,
                    'isAdmin': isAdmin, 'ads': ads})
        elif request.session.get('ownAds', False):
            ads = Ad.findByAdvertiser(request.user)

            return render(request, 'oglasnik/index.html',
                {'form' : form, 'showTable': True, 'isAdvertiser': isAdvertiser,
                    'isAdmin': isAdmin, 'ads': ads})

        return render(request, 'oglasnik/index.html',
            {'form' : form, 'showTable': False, 'isAdvertiser': isAdvertiser, 'isAdmin': isAdmin})

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
                folderPath = ADVERTISERS_ROOT + 'user_' + str(user.id)
                advertisersGrp = Group.objects.get(name='Advertisers')
                advertisersGrp.user_set.add(user)
                advertisersGrp.save()
                user.is_staff = True
                user.save()
                os.mkdir(folderPath)

            login(request,user)
            return redirect(reverse('index'))
    else:
        form = UserRegistrationForm()
    return render(request, 'oglasnik/userRegistration.html', {'form': form})

@login_required
def adDetails(request, id):
    ad = Ad.objects.get(pk=id)
    isOwnAd = (request.user == ad.user)
    adImages = AdsImages.findByAd(ad)

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
                    'isOwnAd': isOwnAd, 'isNewAd': False, 'isDeletedAd': False, 'ad': ad, 'images': adImages}

                return render(request, 'oglasnik/adDetails.html', context)
    else:
        if(isOwnAd):
            form = AdDetailsForm(initial={
                'title':ad.title, 'description': ad.description,
                'price':ad.price, 'categories': ad.category
                })

            context = {'form': form, 'userData': ad.user.email,'isOwnAd': isOwnAd,
                'isNewAd': False, 'isDeletedAd': False, 'ad':ad, 'images': adImages}

            return render(request, 'oglasnik/adDetails.html', context)

        context = {'ad':ad, 'userData': ad.user.email, 'isOwnAd': isOwnAd, 'isNewAd': False,
            'isDeletedAd': False, 'images': adImages}

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
            form = ModifyCategoriesForm(request.POST)
            if form.is_valid():
                categoryName = form.cleaned_data['categoryName']
                category = form.cleaned_data['categories']

                if(request.POST.get('createBtn') != None):
                    if categoryName == '':
                        context = {'form': form, 'isAdmin': isAdmin,
                            'msg': 'Naziv kategorije nemože biti prazna...'}
                        return render(request, 'oglasnik/modifyCategories.html', context)
                    elif Category.exists(categoryName):
                        context = {'form': form, 'isAdmin': isAdmin,
                            'msg': 'Kategorija već postoji...'}
                        return render(request, 'oglasnik/modifyCategories.html', context)
                    else:
                        newCategory = Category(name=categoryName)
                        newCategory.save()
                        context = {'form': form, 'isAdmin': isAdmin,
                            'msg': 'Nova kategorija pohranjena...'}

                        return render(request, 'oglasnik/modifyCategories.html', context)
                if(request.POST.get('updateBtn') != None):
                    if category == None:
                        context = {'form': form, 'isAdmin': isAdmin,
                            'msg': 'Nije odabrana kategorija za izmjenu...'}
                        return render(request, 'oglasnik/modifyCategories.html', context)
                    elif categoryName == '':
                        context = {'form': form, 'isAdmin': isAdmin,
                            'msg': 'Naziv kategorije nemože biti prazna...'}
                        return render(request, 'oglasnik/modifyCategories.html', context)
                    elif Category.exists(categoryName):
                        context = {'form': form, 'isAdmin': isAdmin,
                            'msg': 'Kategorija već postoji...'}
                        return render(request, 'oglasnik/modifyCategories.html', context)
                    else:
                        modifiedCategory = Category.getByName(category)
                        modifiedCategory.name = categoryName
                        modifiedCategory.save()

                        context = {'form': form, 'isAdmin': isAdmin,
                            'msg': 'Kategorija je izmjenjena...'}
                        return render(request, 'oglasnik/modifyCategories.html', context)

                if(request.POST.get('deleteBtn') != None):
                    if category == None:
                        context = {'form': form, 'isAdmin': isAdmin,
                            'msg': 'Nije odabrana kategorija za brisanje...'}
                        return render(request, 'oglasnik/modifyCategories.html', context)
                    else:
                        deletedCategory = Category.getById(category.id)
                        deletedCategory.delete()

                        context = {'form': form, 'isAdmin': isAdmin,
                            'msg': 'Kategorija je izbrisana...'}
                        return render(request, 'oglasnik/modifyCategories.html', context)
                context = {'form': form, 'isAdmin': isAdmin, 'msg': 'TEST...'}
                return render(request, 'oglasnik/modifyCategories.html', context)
        else:
            form = ModifyCategoriesForm()
            context = {'form': form, 'isAdmin': isAdmin}
            return render(request, 'oglasnik/modifyCategories.html', context)
    else:
        context = {'isAdmin': isAdmin, 'msg': 'Nemate pravo pristupiti ovoj stranici...'}
        return render(request, 'oglasnik/modifyCategories.html', context)

@login_required
def manageImages(request, id):
    ad = Ad.objects.get(id=id)
    isOwnAd = (request.user == ad.user)
    adImage = AdsImages(ad=ad)
    adImages = AdsImages.findByAd(ad)
    form = ImageForm()
    if isOwnAd:
        if request.method == 'POST' and isOwnAd:
            if (request.POST.get('uploadBtn') != None):
                form = ImageForm(request.POST, request.FILES, instance=adImage)
                if form.is_valid():
                    form.save()
            if (request.POST.get('delImageBtn') != None):
                selected = request.POST.getlist('imageChkBx')
                for imgId in selected:
                    image = AdsImages.findById(imgId)
                    image.delete()

        context = {'form': form, 'images': adImages, 'ad': ad}
        return render(request, 'oglasnik/manageImages.html', context)
    return redirect(reverse('index'))
