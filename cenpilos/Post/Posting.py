from django.utils import timezone
from itertools import chain
from typing import List

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from cenpilos.forms import PostForm
from cenpilos.models import Post, UserProfile


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
    print(request.POST.get('post_id'))
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.delete()
    return JsonResponse({})