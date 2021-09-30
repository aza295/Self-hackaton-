from django.contrib import admin

from registration.models import User

"""Регистрируем пользователя в админ панели"""
admin.site.register(User)
