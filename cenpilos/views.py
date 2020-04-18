from django.shortcuts import render
from django.views.generic import *

from .BetaUserLogin.login_beta import login_beta_user
from .Dashboard.dashbaord_requests import get_request, post_request
from .Notifications.notification_requests import notifications_get_request
from .Post.Posting import *
from .Profiles.ProfileFunctions import add_friend_profile, remove_friend_profile
from .Profiles.profile_requests import *
from .forms import *
from .Profiles.ProfileFunctions import userExists

# activation account --- user must verify their account before they will be allowed to sign in!
# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         messages.success(request, f'Thank you for confirming your email!')
#         return redirect('login')
#     else:
#         messages.error(request, f'Your activation link is invalid!')
#         return redirect('login')


# VIEW CLASSES #


class RegisterView(View):
    """
    Registration View
    """
    template_name = 'cenpilos/auth/pages/register.html'

    def get(self, request, *args, **kwargs):
        """
        Processes the get request of the registrationView
        """
        # initial form
        form = RegistrationForm()

        # extra variables to be passed to the initial screen
        content = {
            'form': form,  # IMPORTANT! This is the main registration form. DO NOT REMOVE!
            'register': 'active',
            'title': 'Register | Cenpilos Public'
        }
        return render(request, self.template_name, content)

    def post(self, request, *args, **kwargs):
        """
        Processes the post request of the registrationView
        """

        # Double checks to ensure the request method is POST
        if request.method == "POST":
            # passes the registration form with the filled in data for validation
            form = RegistrationForm(request.POST)

            # checks to make sure the form is valid
            if form.is_valid():
                # saves the form data to the User Model
                user = form.save(commit=False)

                # makes the user inactive before they confirm their email address
                user.is_active = False

                # gets the password entered and saves the password
                password = form.cleaned_data['password1']
                user.set_password(password)

                # saves the user
                user.save()

                # # sends the user confirmation email
                # # get the current site
                # current_site = get_current_site(request)
                #
                # to_list = [user.email]
                # username = form.cleaned_data['username']
                # email = form.cleaned_data['email']
                #
                # from_email = settings.EMAIL_HOST_USER
                #
                # message = render_to_string(
                #     'cenpilos/email/basic_email_confirmation.html',
                #     {
                #         'username': username,
                #         'email_address': email,
                #         'domain': get_current_site(request),
                #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                #         'token': account_activation_token.make_token(user),
                #     }
                # )
                # subject = 'Activate your account with Practice Logger -- A service by Cenpilos Public.'
                # html_message = loader.render_to_string(
                #     'cenpilos/email/confirm_email_address.html',
                #     {
                #         'username': username,
                #         'email_address': email,
                #         'domain': get_current_site(request),
                #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                #         'token': account_activation_token.make_token(user),
                #     }
                # )
                # send_mail(subject, message, from_email, to_list, fail_silently=True, html_message=html_message)
                #
                # # Displays visual feedback to let the user know that their account is created
                # messages.warning(request, f'Before you can start using your account, you must'
                #                           f'verify your email before being able to login.')
                # # Redirects the user to the login page
                return redirect('login')
        else:
            # if nothing was done
            form = RegistrationForm()

        # extra variables to be passed to the initial screen
        context = {
            'form': form  # IMPORTANT! This is the main registration form. DO NOT REMOVE!
        }

        return render(request, self.template_name, context)


class DashboardView(View):
    """
    Dashboard View
    """
    template_name = 'cenpilos/dashboard/pages/index.html'

    def get(self, request, *args, **kwargs):
        """
        Processes the get request for the main page.
        """

        if not request.user.is_authenticated:
            return redirect('login')
        else:
            return render(request, self.template_name, get_request(request))

    def post(self, request, *args, **kwargs):
        """
        Processes the post request of the main page.
        """
        if not request.user.is_authenticated:
            return redirect('login')
        return post_request(request)


class ProfileView(View):
    """
    Dashboard View
    """
    template_name = 'cenpilos/dashboard/pages/profile.html'

    def get(self, request, username):
        """
        Processes the get request for the main page.
        """
        try:
            if not request.user.is_authenticated:
                # raise NoReverseMatch
                return redirect('login')
            else:
                return render(request, self.template_name, profile_get_request(request, username))
        except BaseException:
            if not request.user.is_authenticated:
                return redirect('login')
            if not userExists(username):
                return JsonResponse({}, status=404)

    def post(self, request, *args, **kwargs):
        """
        Processes the post request of the main page.
        """

        return render(request, self.template_name, profile_post_request(request))


class NotificationView(View):
    """
    Notification View
    """
    template_name = 'cenpilos/dashboard/pages/notifications.html'

    def get(self, request, *args, **kwargs):
        """
        Executes when the get request is initiated
        :param request: A web request -- usually passed by the form
        :param args: extra arguments
        :param kwargs: extra arguments
        :return:# returns a render method with:
                #   1. request
                #   2. template_name
                #   3. the content variable, containing all the variables to be passed into the views
        """

        if not request.user.is_authenticated:
            return redirect('login')
        else:
            return render(request, self.template_name, notifications_get_request())


# VIEW FUNCTIONS #
def like_post(request):
    """ handles the liking of a post"""
    if not request.user.is_authenticated:
        return redirect('login')
    return like_pPost(request)


def dislike_post(request):
    """ Handles the disliking of a post """

    return dislike_pPost(request)


def delete_post(request):
    """ Handles the deletion of a post """
    if not request.user.is_authenticated:
        return redirect('login')

    return delete(request)


def login_beta(request):
    """ Handles automatic login of beta user"""

    return login_beta_user(request)


def add_friend(request, username):
    """ Handle an addition of a friend """
    try:
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            return add_friend_profile(request, username)
    except BaseException:
        if not request.user.is_authenticated:
            return redirect('login')


def remove_friend(request, username):
    """ Handles the deletion of a friend """
    try:
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            return remove_friend_profile(request, username)
    except BaseException:
        if not request.user.is_authenticated:
            return redirect('login')