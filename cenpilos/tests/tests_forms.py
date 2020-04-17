"""
PROJECT CENPILOS -- Automated Testing Suite

This testing suite is for TESTING forms ONLY.

See tests_views.py for testing the views
See tests_urls.py for tessting the urls
See tests_models.py for testing models

== DESCRIPTION ==
This is created to check the correctness of the code written before release.
ALL FEATURES WILL BE tested to make sure everything is correct DURING every beta release.

Copyright (c) Zhaoyu Guo 2020. All rights reserved.
"""

from django.test import TestCase
from cenpilos.forms import *


class RegistrationFormTest(TestCase):

    def test_form_empty(self):
        """
        A registration form with completely empty data
        """
        form = RegistrationForm(data={
            "email": "",
            "username": "",
            "password1": "",
            "first_name": "",
            "last_name": ""
        })

        self.assertFalse(form.is_valid())

    def test_form_sapces(self):
        """
        A registration form with all spaces
        """
        form = RegistrationForm(data={
            "email": " ",
            "username": " ",
            "password1": " ",
            "first_name": " ",
            "last_name": " "
        })

        self.assertFalse(form.is_valid())


    def test_some_fields_empty(self):
        """
        A registration form with one field filled in
        """
        form = RegistrationForm(data={
            "email": "",
            "username": "fd",
            "password1": "",
            "first_name": "",
            "last_name": ""
        })

        self.assertFalse(form.is_valid())

    def test_all_but_email(self):
        """
        A registration form with one field not filled
        """
        form = RegistrationForm(data={
            "email": "",
            "username": "fd",
            "password1": "eeef",
            "password2": "eeef",
            "first_name": "efe",
            "last_name": "efefef"
        })

        self.assertFalse(form.is_valid())

    def test_all_but_email_space(self):
        """
        A registration form with the email space having a space
        """
        form = RegistrationForm(data={
            "email": " ",
            "username": "fd",
            "password1": "eeef",
            "password2": "eeef",
            "first_name": "efe",
            "last_name": "efefef"
        })

        self.assertFalse(form.is_valid())

    def test_username_greater_than_150(self):
        """
        A registration form with a oversized username
        """
        form = RegistrationForm(data={
            "email": "ggerr@gg.com",
            "username": "fefjhoooooooooooooooooooooooooooooooooooeiofheoifheiofhewoihfewofjewojfewifewpofjpoefoefopfpefefefefefffeerfweheihfiohfoi;hoiefhio;hferwafaefwffeferffeefrerf",
            "password1": "23",
            "password2": "23",
            "first_name": "efe",
            "last_name": "efefef"
        })

        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        """
        A registration form with an invalid email
        """
        form = RegistrationForm(data={
            "email": "ggerr@gg",
            "username": "fd",
            "password1": "eeef",
            "password2": "eeef",
            "first_name": "efe",
            "last_name": "efefef"
        })

        self.assertFalse(form.is_valid())

    def test_valid(self):
        """
        A registration form with all the correct inputs
        """
        form = RegistrationForm(data={
            "email": "ggerr@gg.com",
            "username": "fd",
            "password1": "ithissAValid@",
            "password2": "ithissAValid@",
            "first_name": "efe",
            "last_name": "efefef"
        })

        self.assertTrue(form.is_valid())

    def test_password_less_than_8(self):
        """
        A registration form with a password less than 8 characters
        """
        form = RegistrationForm(data={
            "email": "ggerr@gg.com",
            "username": "fd",
            "password1": "23",
            "password2": "23",
            "first_name": "efe",
            "last_name": "efefef"
        })

        self.assertFalse(form.is_valid())


class TestPostForm(TestCase):

    def test_empty(self):
        """
        A post form with empty data (NO SPACE)
        """

        form = PostForm(data={
            "post_body" : ""
        })

        self.assertFalse(form.is_valid())

    def test_space(self):
        """
        A post form with a space
        """
        form = PostForm(data={
            "post_body": " "
        })

        self.assertFalse(form.is_valid())

    def test_multiple_space(self):
        """
        A post form with multiple spaces
        """
        form = PostForm(data={
            "post_body": "  "
        })

        self.assertFalse(form.is_valid())

    def test_valid(self):
        """
        A post form with valid data
        """
        form = PostForm(data={
            "post_body": "This is a test"
        })

        self.assertTrue(form.is_valid())