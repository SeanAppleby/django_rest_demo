# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from rest_framework.test import APITestCase, APIClient


class ThrottleAPITests(APITestCase):
    fixtures = ['settings.json']

    def test_duplicate_throttle(self):
        client = APIClient()
        client.post('/create_comment', {'username': 'test-user', 'text': "test text", 'content_url': 'test-url', 'ip':'1.160.10.240' }, format='json')
        client.post('/create_comment', {'username': 'test-user', 'text': "test text", 'content_url': 'test-url', 'ip':'1.160.10.240' }, format='json')
        response =client.post('/create_comment', {'username': 'test-user', 'text': "test text", 'content_url': 'test-url', 'ip':'1.160.10.240' }, format='json')
        self.assertEqual(response.status_code, 429)
