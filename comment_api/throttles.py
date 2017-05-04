from __future__ import unicode_literals

from  datetime import datetime
import time

from rest_framework import throttling
from rest_framework.exceptions import Throttled
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import cache as default_cache
from rest_framework.compat import is_authenticated

from comment_api.models import Comment, Setting

class PostThrottle(throttling.BaseThrottle):
    """
    This class is used to throttle post requests based on there criteria:
    - An IP is locked out for posting duplicates of recent comments
    - IPs are locked out for posting comments too rapidly

    The numbers governing these criteria are in the Setting table and accessible through the admin portal
    """
    cache = default_cache
    cache_format = 'throttle_%(scope)s_%(ip)s'
    scope = None
    timer = time.time

    def __init__(self):
        self.get_settings()

    def get_cache_key(self, request, view):
        """
        ip's are hardcoded in request data for development
        """
        ip = request.POST.get('ip')
        return self.cache_format % {
            'scope': self.scope,
            'ip': ip
        }

    def get_settings(self):
        """
        Gets settings from the settings table in database. This should be using caching, but isn't yet.
        """
        duplicate_settings = Setting.objects.get(name='duplicate_settings').value
        duplicate_setting_list = duplicate_settings.split('/')
        self.duplicate_rate = self.parse_setting_time(duplicate_setting_list[0], "duplicate_rate")
        self.duplicate_lockout = self.parse_setting_time(duplicate_setting_list[1], "duplicate_lockout")

        post_rate_settings = Setting.objects.get(name='post_rate_settings').value
        post_rate_setting_list = post_rate_settings.split('/')
        self.post_rate_num = int(post_rate_setting_list[0])
        self.post_rate_time = self.parse_setting_time(post_rate_setting_list[1], "post_rate_time")
        self.post_rate_lockout = self.parse_setting_time(post_rate_setting_list[2], "post_rate_lockout")

    def parse_setting_time(self, setting_value, setting_name):
        """
        This expects a format like "24-h"
        """
        time_symbols = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        try:
            values = setting_value.split('-')
            multiple = values[0]
            symbol = values[1]
            duration = int(time_symbols[symbol] * int(multiple))
            return duration
        except:
            error_detail = 'The field for ' + setting_name + ' is not of the correct format.\nThe throttler expects a format like \"24-h\"'
            raise ImproperlyConfigured(error_detail)


    def is_recent_duplicate(self, request):
        username = request.POST.get('username')
        text = request.POST.get('text')
        content_url = request.POST.get('content_url')

        # Get the latest duplicate comment if there is one, otherwise return false
        try:
            duplicate = Comment.objects.filter(username=username, text=text,content_url=content_url).latest('created_at')

            # Check if the most recent duplicate comment is recent enough to throttle
            if int(datetime.now().strftime("%s")) - int(duplicate.created_at.strftime("%s")) < int(self.duplicate_rate):
                return True
        except:
            return False

    def allow_request(self, request, view):
        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()
        while self.history and self.history[-1][0] <= self.now - float(self.post_rate_time):
            if self.history[-1][1] == 'post':
                self.history.pop()
        if len(self.history) >= self.post_rate_num:
            return self.throttle_failure()

        if self.history and self.history[0][1] == 'duplicate':
            time_remaining = self.history[0][0] - (self.now - float(self.duplicate_lockout))
            if time_remaining > 0:
                raise Throttled(detail="You posted a duplicate comment recently.", wait=time_remaining)
            else:
                self.history.pop(0)

        if self.is_recent_duplicate(request):
            self.history.insert(0, [self.now, 'duplicate'])
            self.cache.set(self.key, self.history, float(self.duplicate_lockout))
            raise Throttled(detail=("that's a duplicate"), wait=(self.duplicate_lockout))

        return self.throttle_success()

    def throttle_success(self):
        """
        Inserts the current request's timestamp along with the key
        into the cache.
        """
        self.history.insert(0, [self.now, "post"])
        self.cache.set(self.key, self.history, float(self.post_rate_lockout))
        return True

    def throttle_failure(self):
        """
        Called when a request to the API has failed due to throttling.
        """
        return False


class CombinedThrottle(throttling.BaseThrottle):
    """
    A simple cache implementation, that only requires `.get_cache_key()`
    to be overridden.
    The rate (requests / seconds) is set by a `throttle` attribute on the View
    class.  The attribute is a string of the form 'number_of_requests/period'.
    Period should be one of: ('s', 'sec', 'm', 'min', 'h', 'hour', 'd', 'day')
    Previous request information used for throttling is stored in the cache.
    """
    cache = default_cache
    timer = time.time
    cache_format = 'combined_throttle_%(scope)s_%(ident)s'
    scope = None


    def __init__(self):
        if not getattr(self, 'rate', None):
            self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)

    def get_cache_key(self, request, view):
        if is_authenticated(request.user):
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

    def get_rate(self):
        """
        Determine the string representation of the allowed request rate.
        """

        try:
            return Setting.objects.get(name="combined_throttle_rate").value
        except KeyError:
            msg = "No default throttle rate set for '%s' scope" % self.scope
            raise ImproperlyConfigured(msg)

    def parse_rate(self, rate):
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>
        """
        if rate is None:
            return (None, None)
        num, period = rate.split('/')
        num_requests = int(num)
        duration = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[period[0]]
        return (num_requests, duration)

    def allow_request(self, request, view):
        """
        Implement the check to see if the request should be throttled.
        On success calls `throttle_success`.
        On failure calls `throttle_failure`.
        """
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            return self.throttle_failure()
        return self.throttle_success()

    def throttle_success(self):
        """
        Inserts the current request's timestamp along with the key
        into the cache.
        """
        self.history.insert(0, self.now)
        self.cache.set(self.key, self.history, self.duration)
        return True

    def throttle_failure(self):
        """
        Called when a request to the API has failed due to throttling.
        """
        return False

    def wait(self):
        """
        Returns the recommended next request time in seconds.
        """
        if self.history:
            remaining_duration = self.duration - (self.now - self.history[-1])
        else:
            remaining_duration = self.duration

        available_requests = self.num_requests - len(self.history) + 1
        if available_requests <= 0:
            return None

        return remaining_duration / float(available_requests)
