from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from views import *


urlpatterns = [
	url(r'^create_comment$', CommentCreateView.as_view()),
	url(r'^list_comments/(?P<content_url>.+)$', CommentListView.as_view()),
]
