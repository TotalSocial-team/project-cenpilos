# creates the tokens used for the confirmation email
import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    """
    Creates a new class called TokenGenerator which
    inherits the class PasswordResetTokenGenerator
    """
    def _make_hash_value(self, user, timestamp):
        return {
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        }


account_activation_token = TokenGenerator()

