# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import pytz


class SenatorialZone(models.Model):
    name = models.CharField(max_length = 350)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ['-date']

class Lga(models.Model):
    senatorialzone = models.ForeignKey(SenatorialZone, on_delete=models.CASCADE)
    name = models.CharField(max_length = 350)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ['-date']


class Account(models.Model):
    lga = models.ForeignKey(Lga, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length = 350)
    phone = models.CharField(max_length = 19)
    password = models.CharField(max_length = 350)
    email = models.EmailField(default = '')
    isAdmin = models.BooleanField(default = False)
    isSuperUser = models.BooleanField(default = False)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ['-date']

class SuperUserAdmin(models.Model):
    superUser = models.ForeignKey(Account, on_delete=models.CASCADE, default=1)
    admin = models.IntegerField()
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.admin)
    
    class Meta:
        ordering = ['-date']

class AdminUser(models.Model):
    admin = models.ForeignKey(Account, on_delete=models.CASCADE, default=1)
    user = models.IntegerField()
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.user)
    
    class Meta:
        ordering = ['-date']
