from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import BooleanField, CharField, FloatField, Model
from rules import add_perm, is_active, is_staff


class Source(Model):
    """
    Root model for an astrophysical source.
    """

    is_active = BooleanField(default=False, help_text="Entries require approval by site staff before they are visible.")

    name = CharField(max_length=32, unique=True, null=False, help_text="Most common name or identifier of the source")

    other_names = CharField(max_length=200, null=True, blank=True, help_text="Other names or identifiers for the source")

    ra = FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(360.0)], verbose_name="RA", help_text="Right Ascension (RA) in decimal degrees"
    )

    dec = FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)], verbose_name="Dec", help_text="Declination (Dec) in decimal degrees"
    )

    def aladin_link(self, survey: str = "P/DSS2/color", fov: float = 0.2) -> str:
        """
        Gets the link to the source on Aladin

        :param survey: Selection of survey image.
        :param fov: Initial field of view.
        :returns: The link to a view of the source's sky location.
        """
        return f"https://aladin.u-strasbg.fr/AladinLite/?target={self.ra}{self.dec:+g}&fov={fov:.1f}&survey={survey}"

    def get_absolute_url(self) -> str:
        return f"/source/{self.pk}/"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


# Rules for database interactions with this source
# Conditions are tested on the user wanting to make the change
add_perm("app.add_source", is_active)
add_perm("app.change_source", is_active)
add_perm("app.delete_source", is_staff)
add_perm("app.view_source", is_active)
