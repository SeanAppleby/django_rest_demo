# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from comment_api.models import Comment, Setting

class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'text', 'content_url', 'created_at')
    pass


class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'value')
    list_editable = ('value',)
    pass


admin.site.register(Setting, SettingAdmin)
admin.site.register(Comment, CommentAdmin)
