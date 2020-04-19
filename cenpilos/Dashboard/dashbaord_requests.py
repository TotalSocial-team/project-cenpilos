from django.shortcuts import redirect

from cenpilos.Blockit.Blockit import getStatus
from cenpilos.Post.Posting import retrieve_posts_for_feed, save_post
from cenpilos.Profiles.SaveProfiles import create_profiles
from cenpilos.forms import PostForm, CommentForm
from cenpilos.models import UserProfile
from cenpilos.scripts import version_info
from cenpilos.scripts.release_notes import display_rnotes


def get_request(request):
    form = PostForm()
    comment_form = CommentForm()

    if not request.user.is_authenticated:
        return redirect('login')

    create_profiles()

    display_notes = display_rnotes()

    confirmed_working, partially_working, upcoming_features = display_notes[0], display_notes[1], display_notes[2]

    # version information
    version = version_info.version_information()
    version_type, stage, v_type, number = version[0], version[1], version[2], version[3]

    # Blockit section
    blockit_status = getStatus()
    protected_status, description, d_colour = blockit_status[0], blockit_status[1], blockit_status[2]

    posts = retrieve_posts_for_feed(request)

    # extra variables to be passed to the initial screen
    return {
        'partial': partially_working,
        'confirmed': confirmed_working,
        'upcoming_features': upcoming_features,
        'stage': stage,
        'type': v_type,
        'number': number,
        'version_type': version_type,
        'protected_status': protected_status,
        'desc': description,
        'colour': d_colour,
        'posts': posts,
        'feed': 'active',
        'comment_form': comment_form,
        'form': form,  # IMPORTANT! This is the main post form. DO NOT REMOVE!
        'friends': [friend for u in UserProfile.objects.filter(user=request.user).all() for friend in u.friends.all()]
    }


def post_request(request):
    # Double checks to ensure the request method is POST
    if request.is_ajax():
        if not request.user.is_authenticated:
            return redirect('login')
        # passes the post form with the filled in data for validation
        form = PostForm(request.POST)

        return save_post(request, form)
    return redirect('dashboard')
