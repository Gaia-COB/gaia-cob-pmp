"""
Contains `django-rules` object-based permissions.

Rules should be put in the model files for a given model,
but it's all done here so it's in one place and easier to remove if you don't want it.

https://github.com/dfunckt/django-rules
"""

import rules
from django.contrib.auth.models import User
from rules import always_allow, is_active, is_staff

from app.models import Cat, Owner


def register_rules():
    """
    Registers the rules that determine who can and can't access which models.
    """

    @rules.predicate
    def is_cat_owner(user: User, cat: Cat):
        """
        Does this user own this cat?

        :param user: User. May not be authenticated, or may not have an 'owner'!
        :param cat: Cat. The cat in question.
        :return: True if the user owns this cat, False otherwise.
        """
        return cat and cat.owner and user == cat.owner.user

    @rules.predicate
    def is_owner(user: User, owner: Owner):
        """
        Is this user the account of this cat owner?

        :param user: User. May not be authenticated, or may not have an 'owner'!
        :param owner: The cat owner in question.
        :return: True if the user is associated with this cat owner, False otherwise.
        """
        return user and user == owner.user

    rules.add_perm("app", always_allow)  # The app always shows up in the admin interface

    rules.add_perm("app.create_cat", is_active)  # Allows us to set people as inactive without deleting
    rules.add_perm("app.edit_cat", is_staff | is_cat_owner)
    rules.add_perm("app.delete_cat", is_staff | is_cat_owner)
    rules.add_perm("app.view_cat", is_active)

    # Owner permissions are more complicated - only owners can view themselves, to hide their address!
    rules.add_perm("app.create_owner", is_active)
    rules.add_perm("app.edit_owner", is_staff | is_owner)
    rules.add_perm("app.delete_owner", is_staff)  # Users can't delete themselves!
    rules.add_perm("app.view_owner", is_staff | is_owner)
