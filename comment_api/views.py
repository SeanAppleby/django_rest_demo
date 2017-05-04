# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from comment_api.models import Comment
from comment_api.serializers import CommentSerializer, DevCommentSerializer
from rest_framework import generics
from rest_framework.throttling import UserRateThrottle
from comment_api.throttles import *


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    throttle_class = UserRateThrottle
    def get_queryset(self):
        content_url= self.kwargs['content_url']
        return Comment.objects.filter(content_url = content_url)


class CommentCreateView(generics.CreateAPIView):
    serializer_class = DevCommentSerializer
    throttle_classes = (PostThrottle,)

    def get_queryset(self):
        return Comment.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
