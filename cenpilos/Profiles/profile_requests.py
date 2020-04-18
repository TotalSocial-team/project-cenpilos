from django.core.exceptions import ImproperlyConfigured
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import *

from cenpilos.Post.Posting import save_post
from cenpilos.Profiles.ProfileFunctions import username_check
from cenpilos.forms import PostForm
from cenpilos.models import *
from cenpilos.scripts import version_info


def profile_get_request(request, username):
    try:

        form = PostForm()

        # version information
        version = version_info.version_information()
        version_type, stage, v_type, number = version[0], version[1], version[2], version[3]

        user = username_check(request, username)

        # extra variables to be passed to the initial screen
        return {
            'posts': Post.objects.filter(author=user.user),
            'profile': 'active',
            'stage': stage,
            'type': v_type,
            'number': number,
            'version_type': version_type,
            'form': form,  # IMPORTANT! This is the main post form. DO NOT REMOVE!
            'user': user.user,
            'logged_in_profile': UserProfile.objects.get(user=request.user),
            'profilepage': user,
            'all_users': [u for u in User.objects.all() if u != request.user],
            'friends': [friend for u in UserProfile.objects.filter(user=request.user).all() for friend in u.friends.all()]
        }
    except (NoReverseMatch, ImproperlyConfigured):
        return JsonResponse({})


def profile_post_request(request):
    # Double checks to ensure the request method is POST
    if request.is_ajax():
        # passes the post form with the filled in data for validation
        form = PostForm(request.POST)

        return save_post(request, form)
