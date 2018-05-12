# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# unique raises django.db.IntegrityError
class Category(models.Model):
    name = models.CharField(max_length = 40, null = False, unique = True)

    def __str__(self):
        return self.name

    @staticmethod
    def getAll():
        return Category.objects.all()

    @staticmethod
    def getByName(name):
        return Category.objects.get(name__contains = name)

class Subcategory(models.Model):
    idCategory = models.ForeignKey(Category, on_delete = models.CASCADE,
        null = False)
    name = models.CharField(max_length = 40, null = False, unique = True)

    @staticmethod
    def getAll():
        return Subcategory.objects.all()

    @staticmethod
    def getByName(name):
        return Subcategory.objects.get(name__contains = name)

class Ad(models.Model):
    IdSubcategory = models.ForeignKey(Subcategory, on_delete = models.CASCADE,
        null = False)
    idUser = models.ForeignKey(User, on_delete = models.CASCADE,
        null = False)

    title = models.CharField(max_length = 40, null = False)
    description = models.TextField()
    price = models.DecimalField(max_digits = 8, decimal_places = 2)
    createDate = models.DateField(auto_now_add = True)

    @staticmethod
    def getAll():
        return Ad.objects.all()

    @staticmethod
    def getByTitle(title):
        return Ad.objects.filter(title__icontains = ('%' + title + '%'))

    @staticmethod
    def getByPricerange(minPrice, maxPrice):
        return Ad.objects.filter(price__gte = minPrice, price__lte = maxPrice)
