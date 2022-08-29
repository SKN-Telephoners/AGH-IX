import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.uuid)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
            + six.text_type(user.tmp_email)
        )


account_activation_token = TokenGenerator()
