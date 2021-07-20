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


class Ward(models.Model):
    lga = models.ForeignKey(Lga, on_delete=models.CASCADE)
    name = models.CharField(max_length = 350)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ['-date']


class PollingUnit(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    name = models.CharField(max_length = 350)
    delimitation = models.CharField(max_length = 50)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ['-date']



class Account(models.Model):
    lga = models.ForeignKey(Lga, on_delete=models.CASCADE, default=1)
    pollingUnit = models.ForeignKey(PollingUnit, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length = 350)
    registrationNumber = models.CharField(max_length = 50)
    username = models.CharField(max_length = 350, default='username')
    image = models.FileField(default=None)
    phone = models.CharField(max_length = 19)
    password = models.CharField(max_length = 350)
    # notificationToken = models.CharField(max_length = 1000, default=None)
    gender = models.CharField(max_length = 19, default='')
    about = models.CharField(max_length = 150, default='Change is inevitable')
    isOldMember = models.BooleanField(default=False)
    email = models.EmailField(default = '')
    isAdmin = models.BooleanField(default = False)
    isSuperUser = models.BooleanField(default = False)
    isVerified = models.BooleanField(default = False)
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








