from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import HttpRequest


class UsernameAdapter(DefaultSocialAccountAdapter):
    """ """

    def populate_user(self, request: HttpRequest, sociallogin, data):
        """
        By default, Django uses an account's username in dropdowns e.t.c.
        SocialAccounts use email instead, so we populate the 'username' with the user's name.

        :param request: The signup request.
        :param sociallogin: The AllAuth social account link.
        :param data: The data from the OAuth provider, uses the fields specified in settings.py.
        """
        super().populate_user(request, sociallogin, data)
        sociallogin.user.username = data["email"]
