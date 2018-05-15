# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Category, Ad
# Register your models here.

@admin.register(Category)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Ad)
class AuthorAd(admin.ModelAdmin):
    list_display = ('category', 'user', 'title', 'price')
