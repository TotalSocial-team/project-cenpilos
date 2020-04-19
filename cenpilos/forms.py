from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *  # imports all of the models -- no need to say models.<model name>


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

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # check to make sure that email does not exist
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError('This email already exists.')

class PostForm(forms.ModelForm):
    """
    Form for the user to post to their newsfeed
    """

    # post body field -- allows the user to write their post in a textarea
    post_body = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'What\'s on your mind?',
                   'rows': 4,
                   'class': 'form-control-lg',
                   'id': 'post-content'}),
        label='')

    # saves the data to the Posts model
    class Meta:
        model = Post
        fields = ['post_body']

class CommentForm(forms.ModelForm):
    """
    Form for the user to comment to their newsfeed
    """

    # post body field -- allows the user to write their post in a textarea
    comment_body = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'What\'s on your mind?',
                   'rows': 2,
                   'class': 'form-control-lg',
                   'id': 'comment-content'}),
        label='')

    # saves the data to the Posts model
    class Meta:
        model = Comment
        fields = ['comment_body']
