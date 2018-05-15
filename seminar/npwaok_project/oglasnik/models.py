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

class Ad(models.Model):
    idcategory = models.ForeignKey(Category, on_delete = models.CASCADE,
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

    @staticmethod
    def getByCategory(categoryName):
        return ad.objects.filter(Idcategory = Category.getByName(categoryName))

    @staticmethod
    def findByFilter(category, title, minPrice, maxPrice):
        queryList = []

        if category != None:
            queryList.append(models.Q(idcategory=category))
        if title != '':
            queryList.append(models.Q(title__icontains=title))
        if minPrice != None:
            queryList.append(models.Q(price__gte=minPrice))
        if maxPrice != None:
            queryList.append(models.Q(price__lte=maxPrice))

        if (len(queryList) == 0):
            return Ad.objects.all()

        query = queryList.pop()

        for q in queryList:
            query &= q

        return Ad.objects.filter(query)
