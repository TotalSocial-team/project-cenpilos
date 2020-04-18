"""
PROJECT CENPILOS -- Automated Testing Suite

This file deals with the setup of ALL testing cases
"""

from django.test import TestCase
from django.utils import timezone

from cenpilos.models import *


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

        self.autotesting_username = "autotestingFriend"
        self.autotesting_friend = User.objects.create(
            email="autotestfriend@cenpilos.tech",
            username=self.autotesting_username
        )

        self.friend_password = "autotesting123friend@"
        self.autotesting_friend.set_password(self.friend_password)
        self.autotesting_friend.save()

        # additional usernames

        self.base_template_name = "cenpilos/dashboard/pages/"
        self.notification_name = 'notifications.html'
        self.dashboard_name = 'index.html'
        self.profile_name = 'profile.html'


class SetupPosts(Setup):
    def setUp(self) -> None:
        super(SetupPosts, self).setUp()
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