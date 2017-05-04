from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from views import *


urlpatterns = [
	url(r'^comment-api$', CommentCreateView.as_view()),
	url(r'^comment-api/(?P<content_url>.+)$', CommentListView.as_view()),
]
