"""
Models for the demo.

Realistically, these should probably be in different files,
with models/__init__.py just importing the models from them.
"""

from auditlog.registry import auditlog
from django.contrib.auth import get_user_model
from django.db.models import SET_NULL, CharField, ForeignKey, IntegerField, Model, TextField

User = get_user_model()  # Import this to get the 'proper' model, if it's been replaced.


class Owner(Model):
    """
    Owns a cat
    """

    name = CharField(max_length=255)
    user = ForeignKey(
        get_user_model(),
        on_delete=SET_NULL,
        null=True,
        related_name="user",
    )
    address = TextField()

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        """
        The URL for the detail view of this specific instance.
        Needs to be kept in sync with `main_menu.py`.

        :returns: The URL for this instance.
        """
        return f"/owners/{self.pk}/"

    def get_absolute_url_if_permitted(self, user: User) -> str:
        """
        Returns the URL but only if the user can view it.

        Useful as if Iommi gets a blank URL for e.g. `cell__url` it skips it.

        :param user: The user to check permissions for.
        :return: The URL if the user can visit it, otherwise a blank string.
        """
        if user.has_perm("app.view_owner", self):
            return self.get_absolute_url()
        else:
            return ""


class Cat(Model):
    """Is a cat"""

    name = CharField(max_length=255)
    age = IntegerField()
    owner = ForeignKey(
        Owner,
        on_delete=SET_NULL,
        null=True,
        related_name="cat_set",
    )

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        """
        The URL for the detail view of this specific instance.
        Needs to be kept in sync with `main_menu.py`.

        :returns: The URL for this instance.
        """
        return f"/cats/{self.pk}/"

    def get_absolute_url_if_permitted(self, user: User) -> str:
        """
        Returns the URL but only if the user can view it.

        Useful as if Iommi gets a blank URL for e.g. `cell__url` it skips it.

        :param user: The user to check permissions for.
        :return: The URL if the user can visit it, otherwise a blank string.
        """
        if user.has_perm("app.view_cat", self):
            return self.get_absolute_url()
        else:
            return ""


auditlog.register(Cat)
auditlog.register(Owner)
