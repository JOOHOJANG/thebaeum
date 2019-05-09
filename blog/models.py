# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
CATEGORY_CHOICES=(
        ('M', '전공/언어'),
        ('W', '실무/개발'),
        ('H','취미'),
        )

class Post(models.Model):
    title = models.CharField(max_length=200)
    tutor_id = models.CharField(max_length=200, default='')
    tutor_name = models.CharField(max_length=200)
    tutor_num = models.DecimalField(max_digits=11, decimal_places=0)
    tutor_career = models.TextField(max_length=10000)
    class_info = models.TextField(max_length=10000)
    category=models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='',
        )
    image = models.ImageField(upload_to='images/')
    
    
class Request(models.Model):
    likes = models.ManyToManyField(User, related_name='likes')
    title = models.CharField(max_length=200)
    writer = models.CharField(max_length=200)
    category=models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='',
        )

class FriendshipRequest(models.Model):
    """ Model to represent friendship requests """
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendship_requests_sent')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendship_requests_received')
    accepted = models.BooleanField(default=False)
    refused = models.BooleanField(default=False)


# class Match(models.Model):
#     parent = models.IntegerField()
#     child = models.IntegerField()
#     text = models.TextField(max_length=10000)
#     email = models.CharField(max_length=200, default='')
#    num = models.DecimalField(max_digits=15, decimal_places=0,attrs={'required': False})