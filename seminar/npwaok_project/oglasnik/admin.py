# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Category, Ad, CustomUser
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'price')

    def get_queryset(self, request):
        qs = super(AdAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(user=request.user.pk)




    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = CustomUser.objects.filter(username=request.user.username)
        return super(AdAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
'''
    def get_readonly_fields(self, request, obj=None):
        readOnlyList = list(self.readonly_fields)

        if obj is not None:
            readOnlyList.append('user')
            if obj.user != request.user:
                readOnlyList.extend(('title', 'category', 'title', 'price', 'description'))
        return tuple(readOnlyList)


    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data['user'] = request.user
        request.GET = data
        return super(AdAdmin, self).add_view(request, form_url="", extra_context=extra_context)

    def has_delete_permission(self, request, obj=None):
        if obj != None:
            return obj.user == request.user

        return super(AdAdmin, self).has_delete_permission(request, obj)

    def get_actions(self, request):
        actions = super(AdAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
'''
