# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import permission_required
from django.conf import settings
import os
from django.dispatch import receiver
from PIL import Image, ExifTags

class CustomUser(User):
    class Meta:
        proxy = True

    def isAdvertiser(self):
            return self.groups.filter(name="Advertisers").exists()

class Category(models.Model):
    name = models.CharField(max_length = 40, null = False, unique = True)

    def __str__(self):
        return self.name

    @staticmethod
    def getAll():
        return Category.objects.all()

    @staticmethod
    def getByName(name):
        try:
            return Category.objects.get(name__contains = name)
        except:
            return None


    @staticmethod
    def getById(id):
        return Category.objects.get(id = id)

    @staticmethod
    def exists(categoryName):
        return Category.objects.filter(name = categoryName).exists()

class Ad(models.Model):
    category = models.ForeignKey(Category, on_delete = models.SET_NULL,
        null = True)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE,
        null = False)

    title = models.CharField(max_length = 40, null = False)
    description = models.TextField()
    price = models.DecimalField(max_digits = 8, decimal_places = 2)
    createDate = models.DateField(auto_now_add = True)

    def existsInDB(self):
        return Ad.objects.filter(pk=self.pk).exists()

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
            queryList.append(models.Q(category=category))
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

    @staticmethod
    def findByAdvertiser(advertiser):
        return Ad.objects.filter(user=advertiser)

def advertisersDirectoryPath(instance, filename):
    return 'advertisers/user_{0}/{1}'.format(instance.ad.user_id, filename)

class AdsImages(models.Model):
    ad = models.ForeignKey(Ad, on_delete = models.CASCADE,
        editable=False, null = False)

    image = models.ImageField(upload_to=advertisersDirectoryPath)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT + str(self.image)))
        super(AdsImages,self).delete(*args,**kwargs)

    @staticmethod
    def findByAd(ad):
        return AdsImages.objects.filter(ad=ad)

    @staticmethod
    def findById(id):
        return AdsImages.objects.get(id=id)

@receiver(models.signals.post_delete, sender=AdsImages)
def deleteImages(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT + str(instance.image))):
            os.remove(os.path.join(settings.MEDIA_ROOT + str(instance.image)))


def rotate_image(filepath):
  try:
    image = Image.open(filepath)
    for orientation in ExifTags.TAGS.keys():
      if ExifTags.TAGS[orientation] == 'Orientation':
            break
    exif = dict(image._getexif().items())

    if exif[orientation] == 3:
        image = image.rotate(180, expand=True)
    elif exif[orientation] == 6:
        image = image.rotate(270, expand=True)
    elif exif[orientation] == 8:
        image = image.rotate(90, expand=True)
    image.save(filepath)
    image.close()
  except (AttributeError, KeyError, IndexError):
    # cases: image don't have getexif
    pass

@receiver(models.signals.post_save, sender=AdsImages)
def update_image(sender, instance, **kwargs):
  if instance.image:
    fullpath = os.path.join(settings.MEDIA_ROOT + str(instance.image))
    rotate_image(fullpath)
