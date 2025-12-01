from django.db.models import CharField, Model


class FluxUnit(Model):
    """
    Model to define units of flux.
    """

    name = CharField(
        max_length=32,
        null=False,
        blank=False,
    )

    astropy = CharField(
        max_length=32,
        null=False,
        blank=False,
    )
