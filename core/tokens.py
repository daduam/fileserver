import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        user_pk = six.text_type(user.pk)
        timestamp = six.text_type(timestamp)
        user_is_active = six.text_type(user.is_active)
        return f"{user_pk}{timestamp}{user_is_active}"


account_activation_token = AccountActivationTokenGenerator()
