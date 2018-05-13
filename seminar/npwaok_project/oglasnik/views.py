# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from forms import userRegistrationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse

def index(request):
    if request.user.is_authenticated:
        #create context
        return HttpResponse("User is logged in...")
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
