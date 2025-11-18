from iommi import Form

from app.models.researcher import Researcher


class ResearcherForm(Form):
    """
    Handles the common setup for researcher-based forms.
    """

    class Meta:
        auto__model = Researcher
