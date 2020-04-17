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

from django.test import TestCase
from django.test import Client
from django.urls import reverse
from cenpilos.models import *
from django.utils import timezone
from cenpilos.forms import *
from django.contrib.auth import *


class Setup(TestCase):
    def setUp(self) -> None:
        """
        This is NOT a test case. This is to setup the required
        testing details

        NOTE: The details ARE NOT accessible from the website
        """
        self.username = "autotesting"
        self.autotesting = User.objects.create(
            email="autotest@cenpilos.tech",
            username=self.username
        )

        self.password = "autotesting123@"
        self.autotesting.set_password(self.password)
        self.autotesting.save()

        self.autotesting_username = "autotesting_friend"
        self.autotesting_friend = User.objects.create(
            email="autotestfriend@cenpilos.tech",
            username=self.autotesting_username
        )

        self.friend_password = "autotesting123friend@"
        self.autotesting_friend.set_password(self.friend_password)
        self.autotesting_friend.save()

        self.base_template_name = "cenpilos/dashboard/pages/"
        self.notification_name = 'notifications.html'
        self.dashboard_name = 'index.html'
        self.profile_name = 'profile.html'


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

    def test_dashboard_POST_non_ajax_login_successful(self):
        """
        Sends a valid username and then a non-ajax POST request
        """
        self.assertTrue(self.client.login(username=self.username, password=self.password))
        data = {
            'post_body': 'Hi There'
        }
        response = self.client.post(reverse('dashboard'), data)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)
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
        # # checks to make sure that it actually saved
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


class TestLikingPost(Setup):

    def setUp(self) -> None:
        """
        This is NOT a test case. This creates a list of posts.
        """
        super(TestLikingPost, self).setUp()

        # friend posts
        five_posts = ["This is made by the autotester # 1", "Post # 2",
                      "Post # 3", "Post # 4", "Post # 5"]

        for post in five_posts:
            autotesting_friend_post = Post.objects.create(
                content=post,
                author=self.autotesting_friend,
                date=timezone.now()
            )
            autotesting_friend_post.save()

        # own posts
        five_posts = ["This is made by the autotester # 2", "Post # 2",
                      "Post # 3", "Post # 876", "Post # 4"]

        for post in five_posts:
            autotesting_post = Post.objects.create(
                content=post,
                author=self.autotesting,
                date=timezone.now()
            )
            autotesting_post.save()

    def test_likePost_no_post_non_authenticated(self):
        """
        Sends a like request from a non-authenticated user with no posts
        """

        response = self.client.post(reverse('like_post'), {'post_id': 2334}, follow=True)

        self.assertEquals(response.status_code, 403)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=403)

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
        Sends a post request to posts when you are non-authenticated with posts queried
        """

        # find post
        first_post = Post.objects.filter(author=self.autotesting, content="This is made by the autotester # 2").all()

        first_post = list(first_post)

        post_id = int(first_post[0].id)

        response = self.client.post(reverse('like_post'), {'post_id': post_id}, follow=True)

        # the user CANNOT like a post when they are logged out
        self.assertEquals(response.status_code, 403)

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


class TestProfilePage(Setup):

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
        Adds a friend without loggin in
        """
        response = self.client.get(reverse('add_friend', args=['doesnotexist']), follow=True)
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)

    def test_addFriend_user_invalid_characters_non_authenticated(self):
        """
        Adds a friend without loggin in with a username containing invalid characters
        """
        response = self.client.get(reverse('add_friend', args=['doest_@3j3i_3!!']), follow=True)
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

    def test_addFriend_no_user_authenticated(self):
        """
        Adds a friend while logged in but the username does not exist
        """
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('add_friend', args=['doesnotexist']), follow=True)
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
        autotest_userProfile = list(
            UserProfile.objects.filter(user=self.autotesting).all())
        self.assertEquals(autotest_userProfile[0].total_friends, 1)
        self.client.logout()