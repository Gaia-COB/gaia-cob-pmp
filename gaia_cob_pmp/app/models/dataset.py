from django.core.validators import MinValueValidator
from django.db.models import CASCADE, BooleanField, FloatField, Model, OneToOneField
from rules import add_perm, is_active, is_staff

from app.models.observation import Observation


class DataSet(Model):
    """
    Details for the Dataset returned from an Observation.
    """

    source = OneToOneField(Observation, on_delete=CASCADE, primary_key=True, related_name="dataset")
