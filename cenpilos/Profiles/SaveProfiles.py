from django.contrib.auth.models import User

from cenpilos.models import UserProfile


def create_profiles() -> None:
    """
    If the user does not have UserProfile Model, this function creates one
    """
    users_userprofile = [userprofile.user for userprofile in UserProfile.objects.all()]
    users = User.objects.all()

    for u in users:
        if u not in users_userprofile:
            userprofile = UserProfile(user=u)
            userprofile.save()
