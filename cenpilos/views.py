from django.contrib import messages
from django.contrib.auth import *
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template import loader
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import *
from django.contrib.auth.models import User

from project_cenpilos import settings
from .forms import *
from .scripts import release_notes, version_info
from .tokens.activation_token import account_activation_token

# activation account --- user must verify their account before they will be allowed to sign in!
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, f'Thank you for confirming your email!')
        return redirect('login')
    else:
        messages.error(request, f'Your activation link is invalid!')
        return redirect('login')


class RegisterView(View):
    """
    Registration View
    """
    template_name = 'cenpilos/auth/pages/register.html'
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
        Executes when the user submits a post request -- usually by clicking a button.
        :param request: A web request -- usually passed by the form
        :param args: extra arguments
        :param kwargs: extra arguments
        :return:# returns a render method with:
                #   1. request
                #   2. template_name
                #   3. the content variable, containing all the variables to be passed into the views
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

                # sends the user confirmation email
                # get the current site
                current_site = get_current_site(request)

                to_list = [user.email]
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']

                from_email = settings.EMAIL_HOST_USER

                message = render_to_string(
                    'cenpilos/email/basic_email_confirmation.html',
                    {
                        'username': username,
                        'email_address': email,
                        'domain': get_current_site(request),
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode,
                        'token': account_activation_token.make_token(user),
                    }
                )
                subject = 'Activate your account with Practice Logger -- A service by Cenpilos Public.'
                html_message = loader.render_to_string(
                    'cenpilos/email/confirm_email_address.html',
                    # TODO: Change the logo of the email template!
                    {
                        'username': username,
                        'email_address': email,
                        'domain': get_current_site(request),
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode,
                        'token': account_activation_token.make_token(user),
                    }
                )
                send_mail(subject, message, from_email, to_list, fail_silently=True, html_message=html_message)

                # Displays visual feedback to let the user know that their account is created
                messages.warning(request, f'Before you can start using your account, you must'
                f'verify your email before being able to login.')
                # Redirects the user to the login page
                return redirect('login')    # TODO: add 'login' to your urls.py file
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

        r_notes = release_notes.read_notes()

        confirmed_working = r_notes[0]

        if not confirmed_working:
            confirmed_working = "None"

        partially_working = r_notes[1]
        if not partially_working:
            partially_working = "None"

        new_features = r_notes[2]
        if not new_features:
            new_features = "None"

        # version information
        version = version_info.version_information()
        version_type = version[0]
        stage = version[1]
        v_type = version[2]
        number = version[3]

        # Blockit section

        # variables
        protected_status = 0
        # protected status, numerical value to value displayed to the user: #
        # if protected_status variable is:
        # 0 == protected (no action needed)
        # 1 == warning to be displayed to the user (might require user to take action)
        # 2 == not protected (immediate action required)

        # displayed underneath the account status
        description = ""

        # the colour of the description
        d_colour = ''

        if protected_status == 0:
            description = 'Great news! We have not found any problems with you account. ' \
                            'However, please check here for regular updates.'
            d_colour = 'success'

        # extra variables to be passed to the initial screen
        content = {
            'partial': partially_working,
            'confirmed': confirmed_working,
            'new_features': new_features,
            'stage': stage,
            'type': v_type,
            'number': number,
            'version_type': version_type,
            'protected_status': protected_status,
            'desc': description,
            'colour': d_colour,
            'feed': 'active',
        }
        return render(request, self.template_name, content)


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

        # version information
        version = version_info.version_information()
        version_type = version[0]
        stage = version[1]
        v_type = version[2]
        number = version[3]

        # extra variables to be passed to the initial screen
        content = {
            'stage': stage,
            'type': v_type,
            'number': number,
            'version_type': version_type,
            'notifications': 'active',
        }
        return render(request, self.template_name, content)
