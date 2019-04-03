from django.contrib.auth.models import User
from django.db import models


# this is where the posts should be saved at
class Posts(models.Model):

    # associates the user with this post
    user_info = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    post_body = models.CharField(max_length=100000)     # user can save up to 1000 characters

    # tags are defined in the following way:
    #       1. <#><tag_name>
    # TODO: Implement truncation logic
    # TODO: Create tag fields
    # TODO: Change the database type before starting the project
