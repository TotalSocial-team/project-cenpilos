"""
PROJECT CENPILOS -- Automated Testing Suite

This testing suite is for TESTING views ONLY.

See tests_forms.py for testing the forms
See tests_urls.py for testing the urls
See tests_models.py for testing models


== DESCRIPTION ==
This is created to check the correctness of the code written before release.
ALL FEATURES WILL BE tested to make sure everything is correct DURING every beta release.


Copyright (c) Zhaoyu Guo 2020. All rights reserved.
"""

import random
import re

from django.core import mail
from django.test import *
from django.urls import reverse

from cenpilos.forms import *
from .SetupTests import *


class TestRegistration(TestCase):

    def test_create_user_full(self):
        """
        Creates a user and checks the confirmation email was sent successfully
        """
        user_data = {
            'user1': ['autotestingUser1',
                      'user123@',
                      'autotestinguser@cenpilos.tech',
                      'AutoTesting',
                      'User']
        }
        response_user1 = self.client.post(reverse('register'), {
            'email': user_data['user1'][2],
            'username': user_data['user1'][0],
            'password1': user_data['user1'][1],
            'password2': user_data['user1'][1],
            'first_name': user_data['user1'][3],
            'last_name': user_data['user1'][4]
        }, follow=True)

        self.assertEquals(response_user1.status_code, 200)
        user = User.objects.filter(email=user_data['user1'][2]).all()
        self.assertRedirects(response_user1, '/login/', status_code=302, target_status_code=200)
        self.assertFalse(user[0].is_active)
        token_regex = r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/'
        email_content = mail.outbox[0].body
        match = re.search(token_regex, email_content)
        # print(match.re)
        self.assertTrue(len(match.groups()) == 2)
        args = [match.group(1), match.group(2)]
        # print(match.)
        activation_response = self.client.post(reverse('activate', kwargs={'uidb64': args[0], 'token': args[1]}),
                                               follow=True)
        self.assertEquals(activation_response.status_code, 200)
        self.assertTrue(user[0].is_active)
        messages = list(activation_response.context['messages'])
        self.assertEquals(len(messages), 0)

    def test_create_two_users_identical_email(self):
        """
        Creates two users with identical email addresses
        """
        user_data = {
            'user1': ['autotestingUser1',
                      'user123@',
                      'autotestinguser@cenpilos.tech',
                      'AutoTesting',
                      'User'],
            'user2': ['autotestingUser2',
                      'user123@1',
                      'autotestinguser@cenpilos.tech',
                      'AutoTesting',
                      'u']
        }
        response_user1 = self.client.post(reverse('register'), {
            'email': user_data['user1'][2],
            'username': user_data['user1'][0],
            'password1': user_data['user1'][1],
            'password2': user_data['user1'][1],
            'first_name': user_data['user1'][3],
            'last_name': user_data['user1'][4]
        }, follow=True)

        response_user2 = self.client.post(reverse('register'), {
            'email': user_data['user2'][2],
            'username': user_data['user2'][0],
            'password1': user_data['user2'][1],
            'password2': user_data['user2'][1],
            'first_name': user_data['user2'][3],
            'last_name': user_data['user2'][4]
        }, follow=True)

        self.assertTrue(response_user1.status_code == 200 and
                        response_user2.status_code == 200)
        self.assertRedirects(response_user1, '/login/', status_code=302, target_status_code=200)
        self.assertTrue(response_user2.redirect_chain == [])
        self.assertEquals(User.objects.all().count(), 1)

    def test_create_multiple_users_full(self):
        """
        Creates multiple users and checks the confirmation email was sent successfully
        """
        user_data = {
            'user1': ['autotestingUser1',
                      'user123@',
                      'autotestinguser@cenpilos.tech',
                      'AutoTesting',
                      'User'],
            'user2': ['autotestingUser2',
                      'user123@1',
                      'autotestinguser1@cenpilos.tech',
                      'AutoTesting',
                      'u'],
            'user3': ['autotestingUser3',
                      'user123@1',
                      'autotestinguser45@cenpilos.tech',
                      'AutoTesting',
                      'u']
        }

        responses = []
        for key in user_data:
            response_user = self.client.post(reverse('register'), {
                'email': user_data[key][2],
                'username': user_data[key][0],
                'password1': user_data[key][1],
                'password2': user_data[key][1],
                'first_name': user_data[key][3],
                'last_name': user_data[key][4]
            }, follow=True)
            self.assertRedirects(response_user, '/login/', status_code=302, target_status_code=200)
            responses.append(response_user)
        users = User.objects.all()
        self.assertTrue(len(responses) == 3 and len(users) == 3 and len(users) == len(responses))

        for r in range(3):
            token_regex = r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/'
            email_content = mail.outbox[r].body
            self.assertFalse(users[r].is_active)
            match = re.search(token_regex, email_content)
            self.assertTrue(len(match.groups()) == 2)
            args = [match.group(1), match.group(2)]
            # print(match.)
            activation_response = self.client.post(reverse('activate', kwargs={'uidb64': args[0], 'token': args[1]}),
                                                   follow=True)
            self.assertEquals(activation_response.status_code, 200)
            user = User.objects.filter(email=users[r].email).all()
            self.assertTrue(user[0].is_active)
            messages = list(activation_response.context['messages'])
            self.assertEquals(len(messages), 0)


class TestDashboard(Setup):

    def test_dashboard_GET_non_authenticated(self):
        """
        Sends a GET request to an non-authenticated dashboard instance
        """
        client = Client()

        response = client.get(reverse('dashboard'), follow=True)

        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

        self.assertTemplateNotUsed(response, self.base_template_name + self.dashboard_name)

    def test_dashboard_POST_non_ajax_non_authenticated(self):
        """
        Sends a non-ajax POST request to an non-authenticated dashboard instance
        """
        client = Client()
        response = client.post(reverse('dashboard'))
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_dashboard_POST_ajax_non_authenticated(self):
        """
        Sends an ajax POST request to an non-authenticated dashboard instance
        """
        data = {
            'post_body': 'Hi There'
        }

        response = self.client.post(reverse('dashboard'), data, **{'HTTP_X_REQUESTED_WITH':
                                                                       'XMLHttpRequest'})

        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_dashboard_GET_login_unsuccessful(self):
        """
        Sends an invalid username and a GET request
        """
        credentials = ['username', 'username']

        self.assertFalse(self.client.login(username=credentials[0], password=credentials[1]))

        response = self.client.get(reverse('dashboard'), follow=True)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_dashboard_GET_login_successful(self):
        """
        Sends valid username and a GET request
        """

        self.assertTrue(self.client.login(username=self.username, password=self.password))

        response = self.client.get(reverse('dashboard'), follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.base_template_name + self.dashboard_name)
        self.assertEquals(response.context["user"].username, self.username)
        self.client.logout()

    def test_dashboard_UserProfilePage_created(self):
        """
        Tests if a UserProfile object has been created for the logged in user
        """
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(reverse('dashboard'), follow=True)
        self.assertEquals(response.status_code, 200)

        autotesting_Profile = UserProfile.objects.filter(user=self.autotesting)
        self.assertEquals(len(list(autotesting_Profile)), 1)
        self.assertEquals(autotesting_Profile[0].user, self.autotesting)
        self.assertFalse(autotesting_Profile[0].verified)
        self.assertTrue(autotesting_Profile[0].total_friends == 0)

    def test_dashboard_POST_non_ajax_login_successful(self):
        """
        Sends a valid username and then a non-ajax POST request
        """
        self.assertTrue(self.client.login(username=self.username, password=self.password))
        data = {
            'post_body': 'Hi There'
        }
        response = self.client.post(reverse('dashboard'), data)
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)
        self.client.logout()

    def test_dashboard_POST_fail_empty_ajax_login_successful(self):
        """
        Sends a valid username and then sends an ajax POST request with invalid data
        """
        body = ""
        self.assertTrue(self.client.login(username=self.username, password=self.password))
        data = {
            'post_body': body
        }
        response = self.client.post(reverse('dashboard'), data, **{'HTTP_X_REQUESTED_WITH':
                                                                       'XMLHttpRequest'})
        self.assertEquals(response.status_code, 400)
        self.assertJSONNotEqual(
            str(response.content, encoding='utf8'),
            {'message': 'Successfully submitted form data.'}
        )

        get_request = self.client.get(reverse('dashboard'), follow=True)
        # # checks to make sure that it DID NOT actually saved
        autotesting_posts = Post.objects.filter(author=get_request.context["user"]).all()
        self.assertEquals(list(autotesting_posts), [])
        self.client.logout()

    def test_dashboard_POST_fail_single_space_ajax_login_successful(self):
        """
        Sends a valid username and then sends an ajax POST request with invalid data
        (a single space)
        """
        body = " "
        self.assertTrue(self.client.login(username=self.username, password=self.password))
        data = {
            'post_body': body
        }
        response = self.client.post(reverse('dashboard'), data, **{'HTTP_X_REQUESTED_WITH':
                                                                       'XMLHttpRequest'})
        self.assertEquals(response.status_code, 400)
        self.assertJSONNotEqual(
            str(response.content, encoding='utf8'),
            {'message': 'Successfully submitted form data.'}
        )

        get_request = self.client.get(reverse('dashboard'), follow=True)

        # # checks to make sure that it DID NOT actually saved
        autotesting_posts = Post.objects.filter(author=get_request.context["user"]).all()
        self.assertEquals(list(autotesting_posts), [])

        self.client.logout()

    def test_dashboard_POST_fail_multiple_spaces_ajax_login_successful(self):
        """
        Sends a valid username and then sends an ajax POST request with invalid data
        (multiple spaces)
        """
        body = "  "
        self.assertTrue(self.client.login(username=self.username, password=self.password))
        data = {
            'post_body': body
        }
        response = self.client.post(reverse('dashboard'), data, **{'HTTP_X_REQUESTED_WITH':
                                                                       'XMLHttpRequest'})
        self.assertEquals(response.status_code, 400)
        self.assertJSONNotEqual(
            str(response.content, encoding='utf8'),
            {'message': 'Successfully submitted form data.'}
        )

        get_request = self.client.get(reverse('dashboard'), follow=True)

        # # checks to make sure that it DID NOT actually saved
        autotesting_posts = Post.objects.filter(author=get_request.context["user"]).all()
        self.assertEquals(list(autotesting_posts), [])

        self.client.logout()

    def test_dashboard_POST_ajax_login_successful(self):
        """
        Sends a valid username and then an ajax POST request
        """
        body = "Hi there"
        self.assertTrue(self.client.login(username=self.username, password=self.password))
        data = {
            'post_body': body
        }

        response = self.client.post(reverse('dashboard'), data, **{'HTTP_X_REQUESTED_WITH':
                                                                       'XMLHttpRequest'})

        self.assertEquals(response.status_code, 200)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'Successfully submitted form data.'}
        )

        get_request = self.client.get(reverse('dashboard'), follow=True)
        # checks to make sure that it actually saved
        autotesting_posts = Post.objects.filter(author=get_request.context["user"]).all()

        for post in autotesting_posts:
            self.assertEquals(post.content, body)
            self.assertEquals(post.author.username, self.username)

    def test_dashboard_POST_multiple_ajax_login_successful(self):
        """
        Sends a valid username and then multiple ajax POST requests
        """
        post_bodies = ["Test1", "Test2", "Test3"]

        self.assertTrue(self.client.login(username=self.username, password=self.password))

        for post_body in post_bodies:
            data = {
                'post_body': post_body
            }

            response = self.client.post(reverse('dashboard'), data, **{'HTTP_X_REQUESTED_WITH':
                                                                           'XMLHttpRequest'})

            self.assertEquals(response.status_code, 200)

            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {'message': 'Successfully submitted form data.'}
            )

        get_request = self.client.get(reverse('dashboard'), follow=True)
        # # checks to make sure that it actually saved
        autotesting_posts = Post.objects.filter(author=get_request.context["user"]).all()

        post_content = []
        for post in autotesting_posts:
            post_content.append(post.content)
            self.assertEquals(post.author.username, self.username)

        self.assertCountEqual(post_content, post_bodies)
        self.client.logout()

    def test_dashboard_POST_multiple_fail_one_invalid_empty_ajax_login_successful(self):
        """
        Sends a valid username then multiple ajax POST requests with one post body being empty
        """
        post_bodies = ["Test1", "", "Test3"]

        self.client.login(username=self.username, password=self.password)

        for post_body in post_bodies:
            data = {
                'post_body': post_body
            }

            response = self.client.post(reverse('dashboard'), data, **{'HTTP_X_REQUESTED_WITH':
                                                                           'XMLHttpRequest'})

            if post_body != "":
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'message': 'Successfully submitted form data.'}
                )
                self.assertEquals(response.status_code, 200)

            else:
                self.assertJSONNotEqual(
                    str(response.content, encoding='utf8'),
                    {'message': 'Successfully submitted form data.'}
                )
                self.assertEquals(response.status_code, 400)

        get_request = self.client.get(reverse('dashboard'), follow=True)
        # # checks to make sure that it actually saved
        autotesting_posts = Post.objects.filter(author=get_request.context["user"]).all()

        post_content = []
        for post in autotesting_posts:
            post_content.append(post.content)
            self.assertEquals(post.author.username, self.username)
        post_bodies.remove("")

        self.assertCountEqual(post_content, post_bodies)
        self.client.logout()

    def test_dashboard_POST_multiple_fail_one_invalid_multiple_spaces_ajax_login_successful(self):
        """
        Sends a valid username then multiple ajax POST requests with one post body having multiple spaces
        """
        post_bodies = ["Test1", "   ", "Test3"]

        self.client.login(username=self.username, password=self.password)

        for post_body in post_bodies:
            data = {
                'post_body': post_body
            }

            response = self.client.post(reverse('dashboard'), data, **{'HTTP_X_REQUESTED_WITH':
                                                                           'XMLHttpRequest'})

            if post_body != "   ":
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'message': 'Successfully submitted form data.'}
                )
                self.assertEquals(response.status_code, 200)

            else:
                self.assertJSONNotEqual(
                    str(response.content, encoding='utf8'),
                    {'message': 'Successfully submitted form data.'}
                )
                self.assertEquals(response.status_code, 400)

        get_request = self.client.get(reverse('dashboard'), follow=True)
        # # checks to make sure that it actually saved
        autotesting_posts = Post.objects.filter(author=get_request.context["user"]).all()

        post_content = []
        for post in autotesting_posts:
            post_content.append(post.content)
            self.assertEquals(post.author.username, self.username)
        post_bodies.remove("   ")

        self.assertCountEqual(post_content, post_bodies)
        self.client.logout()


class TestNotifications(Setup):

    def test_notifications_non_authenticated(self):
        """
        Go to notifications page without logging in
        """

        response = self.client.get(reverse('notifications'), follow=True)

        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)
        self.assertTemplateNotUsed(response, self.base_template_name + self.notification_name)

    def test_notifications_authenticated(self):
        """
        Go to notifications page when you are logged in
        """

        self.assertTrue(self.client.login(username=self.username, password=self.password))

        response = self.client.get(reverse('notifications'), follow=True)
        self.assertTemplateUsed(response, self.base_template_name + self.notification_name)
        self.assertEquals(response.context["user"].username, self.username)


class TestLikePost(SetupPosts):

    def test_likePost_no_post_non_authenticated(self):
        """
        Sends a like request from a non-authenticated user with no posts
        """

        response = self.client.post(reverse('like_post'), {'post_id': 2334}, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_likePost_no_post_queried_authenticated(self):
        """
        Sends a like request from an authenticated user with no posts queried
        """
        id = 1111
        self.client.login(username=self.username, password=self.password)

        response = self.client.post(reverse('like_post'), {'post_id': id}, follow=True)

        self.assertEquals(response.status_code, 404)
        self.client.logout()

    def test_likePost_post_like_post_non_authenticated(self):
        """
        Sends a like request to posts when you are non-authenticated with posts queried
        """

        # find post
        first_post = Post.objects.filter(author=self.autotesting, content="This is made by the autotester # 2").all()

        first_post = list(first_post)

        post_id = int(first_post[0].id)

        response = self.client.post(reverse('like_post'), {'post_id': post_id}, follow=True)

        # the user CANNOT like a post when they are logged out
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_likePost_post_non_existent_authenticated(self):
        """
        Sends a like request from an authenticated user with posts created but none of them match post_id
        """
        post_id = 223

        self.client.login(username=self.username, password=self.password)

        user_post = Post.objects.filter(author=self.autotesting).all()

        # check to make sure none of them match
        for post in user_post:
            self.assertFalse(post.id == post_id)

        response = self.client.post(reverse('like_post'), {'post_id': post_id}, follow=True)

        self.assertEquals(response.status_code, 404)

    def test_likePost_post_like_own_post_once_authenticated(self):
        """
        Sends one like request from an authenticated user to their own posts
        """
        self.client.login(username=self.username, password=self.password)

        first_post = list(
            Post.objects.filter(author=self.autotesting, content="This is made by the autotester # 2").all())

        response = self.client.post(reverse('like_post'), {'post_id': int(first_post[0].id)}, follow=True)

        self.assertEquals(response.status_code, 200)
        # The user SHOULD NOT be liking their own posts
        self.assertEquals(first_post[0].total_likes, 0)
        self.client.logout()

    def test_likePost_post_like_own_post_multiple_times_authenticated(self):
        """
        Sends multiple like requests from an authenticated user to their own posts
        """
        self.client.login(username=self.username, password=self.password)

        posts = list(
            Post.objects.filter(author=self.autotesting).all())

        for p in posts:
            response = self.client.post(reverse('like_post'), {'post_id': int(p.id)}, follow=True)
            self.assertEquals(response.status_code, 200)
            # The user SHOULD NOT be liking their own posts
            self.assertEquals(p.total_likes, 0)

        self.client.logout()

    def test_likePost_post_like_friends_post_once_authenticated(self):
        """
        Sends a single like request from an authenticated user to another user's post
        """
        self.client.login(username=self.username, password=self.password)

        friend_post = list(
            Post.objects.filter(author=self.autotesting_friend, content="Post # 2").all())

        response = self.client.post(reverse('like_post'), {'post_id': friend_post[0].id}, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(friend_post[0].total_likes, 1)
        self.client.logout()

    def test_likePost_post_like_friends_post_multiple_times_authenticated(self):
        """
        Sends multiple like requests from an authenticated user to another user's post
        """

        self.client.login(username=self.username, password=self.password)

        friend_posts = list(
            Post.objects.filter(author=self.autotesting_friend).all())

        for friend_post in friend_posts:
            response = self.client.post(reverse('like_post'), {'post_id': friend_post.id}, follow=True)

            self.assertEquals(response.status_code, 200)
            self.assertEquals(friend_post.total_likes, 1)

        self.client.logout()


class TestDisLikePost(SetupPosts):

    def test_DislikePost_no_post_non_authenticated(self):
        """
        Sends a dislike request from a non-authenticated user with no posts
        """

        response = self.client.post(reverse('dislike_post'), {'post_id': 2334}, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_DislikePost_no_post_queried_authenticated(self):
        """
        Sends a like request from an authenticated user with no posts queried
        """
        id = 1111
        self.client.login(username=self.username, password=self.password)

        response = self.client.post(reverse('dislike_post'), {'post_id': id}, follow=True)

        self.assertEquals(response.status_code, 404)
        self.client.logout()

    def test_DislikePost_post_like_post_non_authenticated(self):
        """
        Sends a dislike request to posts when you are non-authenticated with posts queried
        """

        # find post
        first_post = Post.objects.filter(author=self.autotesting, content="This is made by the autotester # 2").all()

        first_post = list(first_post)

        post_id = int(first_post[0].id)
        self.client.post(reverse('like_post'), {'post_id': post_id}, follow=True)
        response = self.client.post(reverse('dislike_post'), {'post_id': post_id}, follow=True)

        # the user CANNOT like a post when they are logged out
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_DislikePost_post_non_existent_authenticated(self):
        """
        Sends a dislike request from an authenticated user with posts created but none of them match post_id
        """
        post_id = 223

        self.client.login(username=self.username, password=self.password)

        user_post = Post.objects.filter(author=self.autotesting).all()

        # check to make sure none of them match
        for post in user_post:
            self.assertFalse(post.id == post_id)

        self.client.post(reverse('like_post'), {'post_id': post_id}, follow=True)
        response = self.client.post(reverse('dislike_post'), {'post_id': post_id}, follow=True)

        self.assertEquals(response.status_code, 404)

    def test_DislikePost_post_dislike_own_post_once_authenticated(self):
        """
        Sends one dislike request from an authenticated user to their own posts
        """
        self.client.login(username=self.username, password=self.password)

        first_post = list(
            Post.objects.filter(author=self.autotesting, content="This is made by the autotester # 2").all())

        self.client.post(reverse('like_post'), {'post_id': int(first_post[0].id)}, follow=True)

        response = self.client.post(reverse('dislike_post'), {'post_id': int(first_post[0].id)}, follow=True)

        self.assertEquals(response.status_code, 400)
        # The user SHOULD NOT be liking their own posts
        self.assertEquals(first_post[0].total_likes, 0)
        self.client.logout()

    def test_DislikePost_post_dislike_own_post_multiple_times_authenticated(self):
        """
        Sends multiple dislike requests from an authenticated user to their own posts
        """
        self.client.login(username=self.username, password=self.password)

        posts = list(
            Post.objects.filter(author=self.autotesting).all())

        for p in posts:
            self.client.post(reverse('like_post'), {'post_id': int(p.id)}, follow=True)
            response = self.client.post(reverse('dislike_post'), {'post_id': int(p.id)}, follow=True)
            self.assertEquals(response.status_code, 400)
            # The user SHOULD NOT be liking their own posts
            self.assertEquals(p.total_likes, 0)

        self.client.logout()

    def test_DislikePost_post_dislike_friends_post_once_authenticated(self):
        """
        Sends a single dislike request from an authenticated user to another user's post
        """
        self.client.login(username=self.username, password=self.password)

        friend_post = list(
            Post.objects.filter(author=self.autotesting_friend, content="Post # 2").all())

        self.client.post(reverse('like_post'), {'post_id': friend_post[0].id}, follow=True)
        response = self.client.post(reverse('dislike_post'), {'post_id': friend_post[0].id}, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(friend_post[0].total_likes, 0)
        self.client.logout()

    def test_DislikePost_post_dislike_friends_post_multiple_times_authenticated(self):
        """
        Sends multiple dislike requests from an authenticated user to another user's post
        """

        self.client.login(username=self.username, password=self.password)

        friend_posts = list(
            Post.objects.filter(author=self.autotesting_friend).all())

        for friend_post in friend_posts:
            self.client.post(reverse('like_post'), {'post_id': friend_post.id}, follow=True)
            response = self.client.post(reverse('dislike_post'), {'post_id': friend_post.id}, follow=True)

            self.assertEquals(response.status_code, 200)
            self.assertEquals(friend_post.total_likes, 0)

        self.client.logout()


class TestCommentPost(SetupPosts):

    def setUp(self) -> None:
        """
        This is NOT a test case. This is used for setting up the required variables needed to
        be accessed multiple times
        """
        super(TestCommentPost, self).setUp()
        self.all_posts = list(Post.objects.all())
        self.autoesting_posts = list(Post.objects.filter(author=self.autotesting).all())
        self.autotesting_friend_posts = list(Post.objects.filter(author=self.autotesting_friend).all())

        self.all_post_ids = [p.id for p in self.all_posts]
        self.autoesting_post_ids = [p.id for p in self.autoesting_posts]
        self.autotesting_friend_post_ids = [p.id for p in self.autotesting_friend_posts]

    def login(self):
        """
        Logs in the current user
        """
        self.client.login(username=self.username, password=self.password)

    def test_commentPost_no_post_unauthenticated(self):
        """
        Posts a comment on an non-existent post when the user is not authenticated
        """
        post_id = 234
        self.assertNotIn(post_id, self.all_post_ids)
        # sends a comment request
        response = self.client.post(reverse('comment_post'), {'post_id': post_id}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_commentPost_post_exists_unauthenticated(self):
        """
        Posts a comment on an existent post when the user is not authenticated
        """
        post_id = random.choice(self.all_post_ids)
        # sends a comment request
        response = self.client.post(reverse('comment_post'), {'post_id': post_id}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_commentPost_non_existent_post_authenticated(self):
        """
        Posts a comment on a non-existent post when they are authenticated
        """
        self.login()
        post_id = 23343
        self.assertNotIn(post_id, self.all_post_ids)
        response = self.client.post(reverse('comment_post'), {'post_id': post_id}, follow=True)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.redirect_chain, [])
        self.client.logout()

    def test_commentPost_own_post_authenticated(self):
        """
        Posts a comment on their own post when they are authenticated
        """
        self.login()
        post_id = random.choice(self.autoesting_post_ids)
        # get the post with that id
        post_with_post_id = Post.objects.get(id=post_id)
        data = {
            'post_id': post_id,
            'comment_body': 'Hi this is a test comment'
        }
        response = self.client.post(reverse('comment_post'), data, **{'HTTP_X_REQUESTED_WITH':
                                                                          'XMLHttpRequest'}, follow=True)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': "Successfully submitted comment."}
        )

        # make sure that the comment for that post exists
        comments = Comment.objects.get(author=self.autotesting, post=post_with_post_id)
        self.assertEquals(comments.post.id, post_id)
        self.assertEquals(comments.content, "Hi this is a test comment")
        self.assertTrue(comments.total_likes == 0)

    def test_commentPost_others_authenticated(self):
        """
        Posts a variety of comments on existent, but not their own post when they are authenticated
        """
        self.login()
        post_ids = random.sample(self.autotesting_friend_post_ids, 3)
        comments = ['This is a good comment', "very good", "plus me"]
        for pid in post_ids:
            comment = random.choice(comments)
            post = Post.objects.get(id=pid)
            data = {
                'post_id': pid,
                'comment_body': comment
            }
            response = self.client.post(reverse('comment_post'), data, **{'HTTP_X_REQUESTED_WITH':
                                                                              'XMLHttpRequest'}, follow=True)
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {'message': "Successfully submitted comment."}
            )
            comment_check = Comment.objects.get(author=self.autotesting, post=post)
            self.assertEquals(comment_check.post.id, pid)
            self.assertEquals(comment_check.content, comment)
            self.assertTrue(comment_check.total_likes == 0)
        self.client.logout()

    def test_commentPost_random_posts_authenticated(self):
        """
        Posts a variety of comments on randomly selected posts (not their own posts) when they are authenticated
        """
        self.login()
        post_ids = random.sample(self.autotesting_friend_post_ids, 3) + \
                   random.sample(self.autoesting_post_ids, 3)
        comments = ['This is a good comment', "very good", "plus me", "blan blah blah"]
        for pid in post_ids:
            comment = random.choice(comments)
            post = Post.objects.get(id=pid)
            data = {
                'post_id': pid,
                'comment_body': comment
            }
            response = self.client.post(reverse('comment_post'), data, **{'HTTP_X_REQUESTED_WITH':
                                                                              'XMLHttpRequest'}, follow=True)
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {'message': "Successfully submitted comment."}
            )
            comment_check = Comment.objects.get(author=self.autotesting, post=post)
            self.assertEquals(comment_check.post.id, pid)
            self.assertEquals(comment_check.content, comment)
            self.assertTrue(comment_check.total_likes == 0)

        self.client.logout()


class TestDeletePost(SetupPosts):

    def setUp(self) -> None:
        """
        This is NOT a test case. This is used for setting up the required variables needed to
        be accessed multiple times
        """
        super(TestDeletePost, self).setUp()
        self.all_posts = list(Post.objects.all())
        self.autoesting_posts = list(Post.objects.filter(author=self.autotesting).all())
        self.autotesting_friend_posts = list(Post.objects.filter(author=self.autotesting_friend).all())

        self.all_post_ids = [p.id for p in self.all_posts]
        self.autoesting_post_ids = [p.id for p in self.autoesting_posts]
        self.autotesting_friend_post_ids = [p.id for p in self.autotesting_friend_posts]

    def test_deletePost_no_post_unauthenticated(self):
        """
        Deletes a non-existent post when there is no user authenticated
        """
        post_id = 12
        self.assertNotIn(post_id, self.all_post_ids)
        # send a delete request
        response = self.client.post(reverse('delete_post'), {'post_id': post_id}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_deletePost_post_exsists_unauthenticated(self):
        """
        Deletes an existent post when the user is NOT authenticated
        """
        post_id = random.choice(self.all_post_ids)
        # send a delete request
        response = self.client.post(reverse('delete_post'), {'post_id': post_id}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_deletePost_no_post_authenticated(self):
        """
        Deletes a non-existent post when the user is logged in
        """
        self.client.login(username=self.username, password=self.password)
        post_id = 12
        self.assertNotIn(id, self.all_post_ids)
        # send a delete request
        response = self.client.post(reverse('delete_post'), {'post_id': post_id}, follow=True)
        self.assertEquals(response.status_code, 404)
        self.client.logout()

    def test_deletePost_post_exists_other_user_authenticated(self):
        """
        Deletes another user's post when the user is logged in
        """
        self.client.login(username=self.username, password=self.password)
        post_id = random.choice(self.autotesting_friend_post_ids)
        # send a delete request
        response = self.client.post(reverse('delete_post'), {'post_id': post_id}, follow=True)
        self.assertEquals(response.status_code, 403)
        self.client.logout()

    def test_deletePost_post_exists_own_post_authenticated(self):
        """
        Deletes the authenticated user's post.
        """
        self.client.login(username=self.username, password=self.password)
        post_id = random.choice(self.autoesting_post_ids)
        # send a delete request
        response = self.client.post(reverse('delete_post'), {'post_id': post_id}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.client.logout()


class TestProfileFunctions(Setup):

    def test_visit_profile_non_existent_unauthenticated(self):
        """
        Visits a user profile that does not exist without logging in
        """
        response = self.client.get(reverse('profile', args=['doesnotexist']), follow=True)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_visit_profile_non_existent_invalid_characters_unauthenticated(self):
        """
        Visits a user profile page that has invalid characters as the argument
        """
        response = self.client.get(reverse('profile', args=['doest_@3j3i_3!!']), follow=True)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_addFriend_user_non_authenticated(self):
        """
        Adds a friend without logging in
        """
        response = self.client.get(reverse('add_friend', args=['doesnotexist']), follow=True)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_addFriend_user_invalid_characters_non_authenticated(self):
        """
        Adds a friend without loggin in with a username containing invalid characters
        """
        response = self.client.get(reverse('add_friend', args=['doest_@3j3i_3!!']), follow=True)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_removeFriend_user_non_existent_non_authenticated(self):
        """
        Removes a friend without logging in
        """
        response = self.client.get(reverse('remove_friend', args=['doesnotexist']), follow=True)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_removeFriend_user_invalid_characters_non_authenticated(self):
        """
        Removes a friend without loggin in with a username containing invalid characters
        """
        response = self.client.get(reverse('remove_friend', args=['doest_@3j3i_3!!']), follow=True)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_visit_own_profile_page_authenticated(self):
        """
        Visit your own profile page while you are authenticated
        """
        self.client.login(username=self.username, password=self.password)
        # loophole: create a profile page
        self.client.get(reverse('dashboard'), follow=True)

        response = self.client.get(reverse('profile', args=[self.username]), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PostForm)
        self.assertTemplateUsed(response, self.base_template_name + self.profile_name)
        self.client.logout()

    def test_visit_profile_non_existent_invalid_characters_authenticated(self):
        """
        Visits a user profile page that has invalid characters as the argument (authenticated)
        """
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(reverse('profile', args=['doest_@3j3i_3!!']), follow=True)
        self.assertEquals(response.status_code, 404)
        self.client.logout()

    def test_visit_profile_non_existent_valid_characters_authenticated(self):
        """
        Visits a user profile page which corresponds to a non-existent user (authenticated)
        """
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(reverse('profile', args=['doesnotexist']), follow=True)
        self.assertEquals(response.status_code, 404)
        self.client.logout()

    def test_addFriend_no_user_authenticated(self):
        """
        Adds a friend while logged in but the username does not exist
        """
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('add_friend', args=['doesnotexist']), follow=True)
        self.assertEquals(response.status_code, 404)
        self.client.logout()

    def test_addFriend_non_existent_invalid_characters_authenticated(self):
        """
        Adds a friend while logged in but username has invalid characters as the argument (authenticated)
        """
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(reverse('add_friend', args=['doest_@3j3i_3!!']), follow=True)
        self.assertEquals(response.status_code, 404)
        self.client.logout()

    def test_addFriend_themselves_authenticated(self):
        """
        Adds a friend but the user is themselves
        """
        self.client.login(username=self.username, password=self.password)
        self.client.get(reverse('dashboard'), follow=True)
        response = self.client.get(reverse('add_friend', args=[self.username]), follow=True)

        self.assertEquals(response.status_code, 200)
        # get the UserProfile of that user
        autotest_userProfile = list(
            UserProfile.objects.filter(user=self.autotesting).all())
        # the current user CANNOT friend themselves!
        self.assertEquals(autotest_userProfile[0].total_friends, 0)
        self.client.logout()

    def test_addFriend_another_user_valid_user_authenticated(self):
        """
        Adds a friend but the user is NOT the current logged in user
        """
        self.client.login(username=self.username, password=self.password)
        self.client.get(reverse('dashboard'), follow=True)
        response = self.client.get(reverse('add_friend', args=[self.autotesting_username]), follow=True)

        self.assertEquals(response.status_code, 200)
        # get the UserProfile of that user
        testing_userprofiles = list(
            UserProfile.objects.all())
        self.assertEquals(testing_userprofiles[0].total_friends, 1)
        self.assertTrue(testing_userprofiles[0].total_friends == testing_userprofiles[1].total_friends)
        self.assertIn(self.autotesting_friend, list(testing_userprofiles[0].friends.all()))
        self.client.logout()

    def test_addFriend_already_exists_multiple_authenticated(self):
        """
        Adds a friend but the username of that friend already exists as a friend
        """
        self.client.login(username=self.username, password=self.password)
        self.client.get(reverse('dashboard'), follow=True)
        self.client.get(reverse('add_friend', args=[self.autotesting_username]), follow=True)
        response = self.client.get(reverse('add_friend', args=[self.autotesting_username]), follow=True)

        self.assertEquals(response.status_code, 200)
        testing_userprofiles = list(
            UserProfile.objects.all())
        self.assertEquals(testing_userprofiles[0].total_friends, 1)
        self.assertTrue(testing_userprofiles[0].total_friends == testing_userprofiles[1].total_friends)
        self.assertIn(self.autotesting_friend, list(testing_userprofiles[0].friends.all()))
        self.client.logout()

    def test_addFriend_multiple_friends_authenticated(self):
        """
        Addds multiple friends
        """
        self.client.login(username=self.username, password=self.password)

        # create two adtional user objects
        additional_user1 = User.objects.create(
            username="friend1"
        )
        additional_user1.set_password("password1")
        additional_user1.save()

        additional_user2 = User.objects.create(
            username="friend2"
        )
        additional_user2.set_password("password2")
        additional_user2.save()

        self.client.get(reverse('dashboard'), follow=True)

        friend1_response = self.client.post(reverse('add_friend', args=[additional_user1.username]), follow=True)
        friend2_response = self.client.post(reverse('add_friend', args=[additional_user2.username]), follow=True)

        self.assertTrue(friend1_response.status_code == 200 and friend2_response.status_code == 200)
        testing_userprofiles = list(
            UserProfile.objects.all())
        self.assertEquals(testing_userprofiles[0].total_friends, 2)
        self.assertTrue(testing_userprofiles[2].total_friends == testing_userprofiles[3].total_friends)
        self.assertEquals(testing_userprofiles[2].total_friends, 1)
        self.assertTrue(additional_user1 in list(testing_userprofiles[0].friends.all())
                        and additional_user2 in list(testing_userprofiles[0].friends.all()))

        self.client.logout()

    def test_removeFriend_non_existent_invalid_characters_authenticated(self):
        """
        Removes a friend while logged in but username has invalid characters as the argument (authenticated)
        """
        self.client.login(username=self.username, password=self.password)

        response = self.client.post(reverse('remove_friend', args=['doest_@3j3i_3!!']), follow=True)
        self.assertEquals(response.status_code, 404)
        self.client.logout()

    def test_removeFriend_no_user_exists_authenticated(self):
        """
        Removes a friend while logged in but the username does not exist in friend list
        """
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('remove_friend', args=['doesnotexist']), follow=True)
        self.assertEquals(response.status_code, 404)
        self.client.logout()

    def test_removeFriend_user_exists_authenticated(self):
        """
        Renmoves a friend which exists in the friend list
        """
        self.client.login(username=self.username, password=self.password)
        self.client.get(reverse('dashboard'), follow=True)
        self.client.post(reverse('add_friend', args=[self.autotesting_username]), follow=True)
        response = self.client.post(reverse('remove_friend', args=[self.autotesting_username]), follow=True)
        self.assertEquals(response.status_code, 200)
        # get the UserProfile of that user
        testing_userprofiles = list(
            UserProfile.objects.all())
        self.assertEquals(testing_userprofiles[0].total_friends, 0)
        self.assertTrue(testing_userprofiles[0].total_friends == testing_userprofiles[1].total_friends)
        self.assertNotIn(self.autotesting_friend, list(testing_userprofiles[0].friends.all()))
        self.client.logout()

    def test_removeFriend_friends_exists_multiple_friends_authenticated(self):
        """
        Removes only one user from the friend list
        """
        self.client.login(username=self.username, password=self.password)

        # create two adtional user objects
        additional_user1 = User.objects.create(
            username="friend1"
        )
        additional_user1.set_password("password1")
        additional_user1.save()

        additional_user2 = User.objects.create(
            username="friend2"
        )
        additional_user2.set_password("password2")
        additional_user2.save()

        self.client.get(reverse('dashboard'), follow=True)
        self.client.post(reverse('add_friend', args=[additional_user1.username]), follow=True)
        self.client.post(reverse('add_friend', args=[additional_user2.username]), follow=True)

        friend1_response = self.client.post(reverse('remove_friend', args=[additional_user1.username]), follow=True)

        self.assertTrue(friend1_response.status_code == 200)
        testing_userprofiles = list(
            UserProfile.objects.all())
        self.assertEquals(testing_userprofiles[0].total_friends, 1)
        self.assertFalse(testing_userprofiles[2].total_friends == testing_userprofiles[3].total_friends)
        self.assertEquals(testing_userprofiles[2].total_friends, 0)
        self.assertFalse(additional_user1 in list(testing_userprofiles[0].friends.all())
                         and additional_user2 in list(testing_userprofiles[0].friends.all()))

        self.client.logout()

    def test_removeFriend_multiple_friends_exists_authenticated(self):
        """
        Removes multiple friends that is in the friend list
        """
        self.client.login(username=self.username, password=self.password)

        # create two adtional user objects
        additional_user1 = User.objects.create(
            username="friend1"
        )
        additional_user1.set_password("password1")
        additional_user1.save()

        additional_user2 = User.objects.create(
            username="friend2"
        )
        additional_user2.set_password("password2")
        additional_user2.save()

        self.client.get(reverse('dashboard'), follow=True)
        self.client.post(reverse('add_friend', args=[additional_user1.username]), follow=True)
        self.client.post(reverse('add_friend', args=[additional_user2.username]), follow=True)

        friend1_response = self.client.post(reverse('remove_friend', args=[additional_user1.username]), follow=True)
        friend2_response = self.client.post(reverse('remove_friend', args=[additional_user2.username]), follow=True)

        self.assertTrue(friend1_response.status_code == 200 and friend2_response.status_code == 200)
        testing_userprofiles = list(
            UserProfile.objects.all())
        self.assertEquals(testing_userprofiles[0].total_friends, 0)
        self.assertTrue(testing_userprofiles[2].total_friends == testing_userprofiles[3].total_friends)
        self.assertEquals(testing_userprofiles[2].total_friends, 0)
        self.assertFalse(additional_user1 in list(testing_userprofiles[0].friends.all())
                         and additional_user2 in list(testing_userprofiles[0].friends.all()))

        self.client.logout()
