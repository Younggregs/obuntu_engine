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
    code = models.CharField(max_length = 3, default="")
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
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, default=1)
    pollingUnit = models.ForeignKey(PollingUnit, on_delete=models.CASCADE, default=1)
    internalId = models.CharField(max_length=50, default=None)
    image = models.FileField(default=None)
    password = models.CharField(max_length = 350)
    firstname = models.CharField(max_length = 350,  default='')
    middlename = models.CharField(max_length = 350 , default='')
    lastname = models.CharField(max_length = 350, default='')
    phone = models.CharField(max_length = 19, default='')
    gender = models.CharField(max_length = 19, default='')
    votercard = models.CharField(max_length = 150, default='')
    age = models.CharField(max_length = 150, default='')
    registrationNumber = models.CharField(max_length = 50)
    isOldMember = models.BooleanField(default=False)
    # email = models.EmailField(default = '')
    isAdmin = models.BooleanField(default = False)
    isSuperUser = models.BooleanField(default = False)
    isVerified = models.BooleanField(default = False)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.firstname)
    
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








# Demo mobile app Models

class DemoAccount(models.Model):
    lga = models.ForeignKey(Lga, on_delete=models.CASCADE, default=1)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, default=1)
    pollingUnit = models.ForeignKey(PollingUnit, on_delete=models.CASCADE, default=1)
    internalId = models.CharField(max_length=50, default=None)
    image = models.FileField(default=None)
    password = models.CharField(max_length = 350)
    firstname = models.CharField(max_length = 350,  default='')
    middlename = models.CharField(max_length = 350 , default='')
    lastname = models.CharField(max_length = 350, default='')
    phone = models.CharField(max_length = 19, default='')
    gender = models.CharField(max_length = 19, default='')
    votercard = models.CharField(max_length = 150, default='')
    age = models.CharField(max_length = 150, default='')
    registrationNumber = models.CharField(max_length = 50)
    isOldMember = models.BooleanField(default=False)
    # email = models.EmailField(default = '')
    isAdmin = models.BooleanField(default = False)
    isSuperUser = models.BooleanField(default = False)
    isVerified = models.BooleanField(default = False)
    office = models.CharField(max_length = 350, default='')
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.firstname)
    
    class Meta:
        ordering = ['-date']


class Post(models.Model):
    account = models.ForeignKey(DemoAccount, on_delete=models.CASCADE, default=1)
    body = models.TextField()
    title = models.TextField()
    image = models.FileField(default=None)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-date']


class PostUpdate(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField(default = timezone.now)


class Comment(models.Model):
    account = models.ForeignKey(DemoAccount, on_delete=models.CASCADE, default=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=1)
    text = models.TextField()    
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.text)

    class Meta:
        ordering = ['-date']



class Like(models.Model):
    account = models.ForeignKey(DemoAccount, on_delete=models.CASCADE, default=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField(default = timezone.now)

    class Meta:
        ordering = ['-date']








