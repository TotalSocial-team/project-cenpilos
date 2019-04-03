from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from .models import *   # imports all of the models -- no need to say models.<model name>


class RegistrationForm(UserCreationForm):
    """
    Additional Fields -- NOT included in the stock UserCreationForm
    """

    # email field
    email = forms.EmailField()

    # first name field
    first_name = forms.CharField(
        widget=forms.TextInput()
    )

    # last name field
    last_name = forms.CharField(
        widget=forms.TextInput()
    )

    # A sub class handling the saving of the data posted to the RegistrationForm
    class Meta:
        # defines the model as User --> This will determine which model the
        # data will be posted to
        model = User

        # this defines which fields should be saved
        fields = ['username', 'email', 'first_name', 'last_name', 'password1']


class PostForm(forms.ModelForm):
    """
    Form for the user to post to their newsfeed
    """

    # post body field -- allows the user to write their post in a textarea
    post_body = forms.CharField(widget=forms.Textarea)

    # saves the data to the Posts model
    class Meta:
        model = Posts
        # TODO: Find a better way to implement this
        fields = ['post_body']
