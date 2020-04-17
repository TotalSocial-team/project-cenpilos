from django.contrib.auth.models import User
from django.http import JsonResponse

from cenpilos.models import UserProfile


def username_check(request, username):

    if not username:
        return UserProfile.objects.get(user=request.user)
    else:
        u = User.objects.get(username=username)
        return UserProfile.objects.get(user=u)


def add_friend_profile(request, username):
    # search for the user that has username
    username_param = User.objects.get(username=username)

    # adds the friends
    logged_in_profile = UserProfile.objects.get(user=request.user)
    username_profile = UserProfile.objects.get(user=username_param)

    if username_param not in logged_in_profile.friends.all() and request.user not in username_profile.friends.all():
        logged_in_profile.friends.add(username_param)
        username_profile.friends.add(request.user)
        logged_in_profile.save()
        username_profile.save()

    return JsonResponse({})


def remove_friend_profile(request, username):
    # search for the user that has username
    username_param = User.objects.get(username=username)

    # adds the friends
    logged_in_profile = UserProfile.objects.get(user=request.user)
    username_profile = UserProfile.objects.get(user=username_param)

    if username_param  in logged_in_profile.friends.all() and request.user in username_profile.friends.all():
        logged_in_profile.friends.remove(username_param)
        username_profile.friends.remove(request.user)

    return JsonResponse({})
