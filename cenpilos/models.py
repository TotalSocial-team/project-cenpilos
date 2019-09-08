from django.contrib.auth.models import User
from django.db import models
import datetime
from django.template.defaultfilters import slugify


class Post(models.Model):

    # associates the user with this post
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    content = models.CharField(max_length=100000)     # user can save up to 1000 characters

    date = models.DateTimeField()

    likes = models.ManyToManyField(User, related_name='likes')

    @property
    def total_likes(self) -> int:
        """
        Likes for the company
        :return: Integer: Likes for the company
        """
        return self.likes.count()


class Comment(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    content = models.CharField(max_length=100000)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=0)

    date = models.DateTimeField()

    likes = models.IntegerField(default=0)