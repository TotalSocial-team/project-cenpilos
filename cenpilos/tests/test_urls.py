"""
PROJECT CENPILOS -- Automated Testing Suite

This testing suite is for TESTING urls ONLY.

See tests_views.py for testing the views
See tests_forms.py for testing the forms
See tests_models.py for testing models

== DESCRIPTION ==
This is created to check the correctness of the code written before release.
ALL FEATURES WILL BE tested to make sure everything is correct DURING every beta release.

Copyright (c) Zhaoyu Guo 2020. All rights reserved.
"""

from django.test import TestCase
from django.urls import reverse, resolve
from cenpilos.views import *
from django.contrib.auth import views as auth_views


class TestUrls(TestCase):

    def test_registration_url_resolved(self):
        """
        Tests to make sure that the registration url is resolved
        """
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, RegisterView)

    def test_login_url_resolved(self):
        """
        Tests to make sure that the login url is resolved
        """
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_url_resolved(self):
        """
        Tests to make sure that the logout url is resolved
        """
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, auth_views.LogoutView)

    def test_dashboard_url_resolved(self):
        """
        Tests to make sure that the dashboard url is resolved
        """
        url = reverse('dashboard')
        self.assertEquals(resolve(url).func.view_class, DashboardView)

    def test_like_post_url_resolved(self):
        """
        Tests to make sure that the like_post url is resolved
        """
        url = reverse('like_post')
        self.assertEquals(resolve(url).func, like_post)

    def test_dislike_post_url_resolved(self):
        """
        Tests to make sure that the dislike_post url is resolved
        """
        url = reverse('dislike_post')
        self.assertEquals(resolve(url).func, dislike_post)

    def test_delete_post_url_resolved(self):
        """
        Tests to make sure that the delete_post url is resolved
        """
        url = reverse('delete_post')
        self.assertEquals(resolve(url).func, delete_post)

    def test_login_beta_url_resolved(self):
        """
        Tests to make sure that the login-beta url is resolved
        """
        url = reverse('login-beta')
        self.assertEquals(resolve(url).func, login_beta)

    def test_profile_url_resolved(self):
        """
        Tests to make sure that the profile url is resolved
        """
        url = reverse('profile', args=['username'])
        self.assertEquals(resolve(url).func.view_class, ProfileView)

    def test_notifications_url_resolved(self):
        """
        Tests to make sure that the notifications url is resolved
        """
        url = reverse('notifications')
        self.assertEquals(resolve(url).func.view_class, NotificationView)

    def test_add_friend_url_resolved(self):
        """
        Tests to make sure that the add_friend url is resolved
        """
        url = reverse('add_friend', args=['some_user'])
        self.assertEquals(resolve(url).func, add_friend)

    def test_remove_friend_url_resolved(self):
        """
        Tests to make sure that the remove_friend url is resolved
        """
        url = reverse('remove_friend', args=['some_user'])
        self.assertEquals(resolve(url).func, remove_friend)

    def test_comment_url_resolved(self):
        """
        Tests to make sure that the comment url is resolved
        """
        url = reverse('comment_post')
        self.assertEquals(resolve(url).func, comment_post)




