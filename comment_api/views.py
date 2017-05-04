# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from comment_api.models import Comment
from comment_api.serializers import CommentSerializer, DevCommentSerializer
from rest_framework import generics
from rest_framework.throttling import UserRateThrottle
from comment_api.throttles import *


class CommentListView(generics.ListAPIView):
    """
    Basic api view for listing comments by a given content url.
    example: "curl <base_url>/comment-api/pop-quiz" will return all comments for pop-quiz content
    """
    serializer_class = CommentSerializer
    throttle_class = UserRateThrottle
    def get_queryset(self):
        content_url= self.kwargs['content_url']
        return Comment.objects.filter(content_url = content_url)


class CommentCreateView(generics.CreateAPIView):
    """
    Basic api view for submitting comments through the endpoint  <base_url>/comment-api
    example data: {"username":"test_user","text":"test comment","content_url":"pop-quiz","ip":"1.160.10.240"}
    """
    serializer_class = DevCommentSerializer
    throttle_classes = (PostThrottle,)

    def get_queryset(self):
        return Comment.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
