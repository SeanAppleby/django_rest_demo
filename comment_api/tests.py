# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from rest_framework.test import APITestCase, APIClient


class APIRequestTests(APITestCase):
    fixtures = ['test_data.json']

    def test_get_comment(self):
        """
        Verify that we can retrieve comments from urls
        """
        client = APIClient()
        response = client.get('/comment-api/test_content')
        response.render()
        self.assertEqual(response.content, '[{"username":"test_user","text":"test_comment","content_url":"test_content"}]')

    def test_post(self):
        """
        Verify that we can post new comments
        """
        client = APIClient()
        request_data = {'username': 'test-user', 'text': "test text", 'content_url': 'test-url', 'ip':'1.160.10.241' }
        response_data = {'username': 'test-user', 'text': "test text", 'id': 2, 'content_url': 'test-url'}
        response =client.post('/comment-api', request_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, response_data)


class ThrottleAPITests(APITestCase):
    fixtures = ['test_data.json']

    def test_deny_duplicate(self):
        """
        An IP address that submits a comment that is a duplicate of another submitted within 24 hours should be locked out
        """
        client = APIClient()
        first_ip_data =  {'username': 'test-user', 'text': "test text", 'content_url': 'test-url', 'ip':'1.160.10.240' }
        second_ip_data = {'username': 'test-user', 'text': "test text", 'content_url': 'test-url', 'ip':'1.160.10.241' }
        locked_out_request_data = {'username': 'test-user', 'text': "test text 2", 'content_url': 'test-url', 'ip':'1.160.10.241' }
        client.post('/comment-api', first_ip_data, format='json')
        duplicate_response = client.post('/comment-api', second_ip_data , format='json')
        self.assertEqual(duplicate_response.status_code, 429)

    def test_duplicate_throttle(self):
        """
        An IP address that submits a comment that is a duplicate of another submitted within 24 hours should be locked out
        """
        client = APIClient()
        first_ip_data =  {'username': 'test-user', 'text': "test text", 'content_url': 'test-url', 'ip':'1.160.10.240' }
        second_ip_data = {'username': 'test-user', 'text': "test text", 'content_url': 'test-url', 'ip':'1.160.10.241' }
        locked_out_request_data = {'username': 'test-user', 'text': "test text 2", 'content_url': 'test-url', 'ip':'1.160.10.241' }
        client.post('/comment-api', first_ip_data, format='json')
        locked_out_response = client.post('/comment-api', locked_out_request_data , format='json')
        self.assertEqual(locked_out_response.status_code, 429)


    def test_post_rate_throttle(self):
        """
        An IP address that submits more than 2 comments in 1 minute should be locked out
        """
        client = APIClient()
        client.post('/comment-api', {'username': 'test-user', 'text': "test text_1", 'content_url': 'test-url', 'ip':'1.160.10.240' }, format='json')
        client.post('/comment-api', {'username': 'test-user', 'text': "test text_2", 'content_url': 'test-url', 'ip':'1.160.10.240' }, format='json')
        response = client.post('/comment-api', {'username': 'test-user', 'text': "test text_3", 'content_url': 'test-url', 'ip':'1.160.10.240' }, format='json')
        self.assertEqual(response.status_code, 429)

    def test_get_rate_throttle(self):
        """
        A user who submits more than 20 requests per minute should be locked out
        """
        client = APIClient()
        for i in range(0, 20):
            response = client.get('/comment-api/test_content')
        self.assertEqual(response.status_code, 429)

    def test_combined_rate_throttle(self):
        """
        A user who submits more than 20 requests per minute should be locked out
        """
        client = APIClient()
        for i in range(0, 19):
            response = client.get('/comment-api/test_content')
            print(response)
        response= client.post('/comment-api', {'username': 'test-user', 'text': "test text_1", 'content_url': 'test-url', 'ip':'1.160.10.240' }, format='json')
        self.assertEqual(response.status_code, 429)
