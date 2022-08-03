# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
 
 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.TextField(verbose_name='Контрагент')
    position = models.TextField(verbose_name='Должность')
 
    def __unicode__(self):
        return self.user
 
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
