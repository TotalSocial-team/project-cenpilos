from itertools import chain
from typing import List

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from cenpilos.forms import *
from cenpilos.models import *


def save_post(request, form: PostForm) -> JsonResponse:
    # checks to make sure the form is valid
    if form.is_valid():

        # don't save the data immediately.
        post = form.save(commit=False)

        # saves the post's content
        content = form.cleaned_data['post_body'].strip()
        #
        post.content = content
        post.author = request.user
        # A minor change to omit autotesting warning
        post.date = timezone.now()
        post.save()
        data = {
            'message': "Successfully submitted form data."
        }
        return JsonResponse(data)
    else:
        return JsonResponse(form.errors, status=400)


def retrieve_posts_for_feed(request) -> List[object]:
    # retrieve the post data
    user_posts = Post.objects.filter(author=request.user).all()

    curr_profile = UserProfile.objects.filter(user=request.user).all()

    friend_posts = []

    # adds the friend's post as well
    for profile in curr_profile:
        friends = profile.friends.all()
        for friend in friends:
            friend_posts += Post.objects.filter(author=friend)

    return list(chain(user_posts, friend_posts))


def like_pPost(request):
    post = get_object_or_404(Post, id=request.POST['post_id'])

    if request.user in post.likes.all():
        return JsonResponse({}, status=400)
    elif post.author == request.user:
        return JsonResponse({})
    else:
        post.likes.add(request.user)
        post.save()
        return JsonResponse({})


def dislike_pPost(request):
    post = get_object_or_404(Post, id=request.POST['post_id'])

    # removes the user from the list of liked users
    if request.user not in post.likes.all():
        return JsonResponse({}, status=400)
    else:
        post.likes.remove(request.user)
        post.save()
        return JsonResponse({})


def delete(request):
    all_posts = [p for p in list(Post.objects.all())]
    logged_in_user_posts = [p for p in list(Post.objects.filter(author=request.user).all())]

    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if (post in all_posts and post not in logged_in_user_posts):
        return JsonResponse({}, status=403)
    post.delete()
    return JsonResponse({})


def comment(request):
    post = get_object_or_404(Post, id=request.POST['post_id'])
    if request.is_ajax():
        if not request.user.is_authenticated:
            return redirect('login')
        # passes the post form with the filled in data for validation
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.content = form.cleaned_data['comment_body'].strip()
            comment.author = request.user
            # A minor change to omit autotesting warning
            comment.date = timezone.now()
            comment.post = post
            comment.save()
            data = {
                'message': "Successfully submitted comment."
            }
            return JsonResponse(data)
        else:
            return JsonResponse(form.errors, status=400)
    return redirect('dashboard')
