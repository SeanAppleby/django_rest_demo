# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from datetime import timedelta


class Comment(models.Model):
    """
    In actual use username and content_url would be foreign keys, but they're set as charfields for proof of concept
    """
    username = models.CharField(max_length=200)
    text = models.TextField()
    content_url = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['created_at']


class Setting(models.Model):
    """
    A table for settings allows an administator to adjust desired settings without rebooting the app.
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    value = models.CharField(max_length=200)
