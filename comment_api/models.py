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


# class TimeoutSetting(dbsettings.Group):
#     post_rate_limit = dbsettings.StringValue(
#         'maximum number of comment posts per second(s), minute(m), hour(h) or day(d) for a user',
#          default='2/m')
#
#     post_rate_timeout = dbsettings.DurationValue(
#         'the amount of time a user is lockedout for exceeding post_rate_limit',
#         default=timedelta(minutes=5))
#
#     duplicate_rate_limit = dbsettings.DurationValue(
#         'the minimum time between duplicate comments',
#         default=timedelta(hours=24))
#
#     duplicate_timeout = dbsettings.DurationValue(
#         'the time for which an account is locked out for posting duplicate comments',
#         default=timedelta(minutes=1))


class Setting(models.Model):
    """
    A table for settings allows an administator to adjust desired settings without rebooting the app.
    """
    name = models.CharField(max_length=200, primary_key=True)
    description = models.TextField()
    value = models.CharField(max_length=200)
