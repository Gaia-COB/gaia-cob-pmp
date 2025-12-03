from iommi import Form

from app.models import DataSet, Observation

class DatasetForm(Form):
    class Meta:
        auto__model = DataSet


class ObservationForm(Form):
    """
    Handles the common setup for project-based forms.
    """

    class Meta:
        auto__model = Observation
