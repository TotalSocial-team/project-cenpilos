from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Post(models.Model):

    # associates the user with this post
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    content = models.CharField(max_length=100000)     # user can save up to 1000 characters

    date = models.DateTimeField()

    likes = models.ManyToManyField(User, related_name='likes')

    @property
    def total_likes(self) -> int:
        """
        Likes for the post
        :return: Integer: Likes for the company
        """
        return self.likes.count()

    def __str__(self):
        """
        The string representation of this
        model
        """
        return self.content + " by: " + self.author.username


class Comment(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    content = models.CharField(max_length=100000)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=0)

    date = models.DateTimeField()

    likes = models.IntegerField(default=0)


class UserProfile(models.Model):
    """
    Represents all the user's information, # of friends, etc...
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    friends = models.ManyToManyField(User, related_name='friends')

    verified = models.BooleanField(default=False)

    gender = models.CharField(max_length=100, blank=True)

    blocked_users = models.ManyToManyField(User, related_name='blocked_users')

    @property
    def total_friends(self) -> int:
        """
        :return: the total number of friends this user has
        """
        return self.friends.count()

    def __str__(self):
        """
        :return: a string representation of this model
        """
        return self.user.username + "'s " + 'Profile.'

    @property
    def get_friends(self) -> list:
        """
        Returns the friends of this particular user
        """
        return self.friends.all()

    @property
    def get_verified_status(self) -> bool:
        """
        Returns the current verified status of this particular user
        """
        return self.verified

    @property
    def get_blocked_users(self) -> list:
        """
        Returns a list of all blocked user blocked by this user
        """
        return self.blocked_users.all()


class Notifications(models.Model):
    """
    Represents a single notification sent by specific events
    """

    # the user that does a specific action
    notifying_user = models.ForeignKey(User, on_delete=models.CASCADE, default=0, related_name="notifying_users")

    # the receiving user of that notification
    receiving_user = models.ForeignKey(User, on_delete=models.CASCADE, default=0, related_name="receiving_user")

    # the date the notification was sent.
    date = models.DateTimeField()

    # whether or not the notification is read or not
    read = models.BooleanField(default=False)

    # the notification content
    content = models.CharField(max_length=1000)

    def __str__(self):

        return self.content