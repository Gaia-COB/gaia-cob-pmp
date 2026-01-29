from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    RESTRICT,
    BooleanField,
    FloatField,
    ForeignKey,
    Model,
    TextField,
)
from rules import add_perm, is_active, is_staff, predicate

from app.models.proposal import Proposal
from app.models.source import Source


class Observation(Model):
    """
    Model for an observation instance.
    """

    source = ForeignKey(Source, on_delete=RESTRICT, help_text="The source which was observed.")

    proposal = ForeignKey(
        Proposal,
        on_delete=CASCADE,
        help_text="The proposal to which this observation is affiliated.",
    )

    is_valid = BooleanField(
        default=False, help_text="Entries require approval by site staff before they are visible."
    )

    jd = FloatField(
        verbose_name="Observation date (JD)",
        help_text="The date and time of the observation, given in JD.",
        null=True,
        blank=True,
    )

    comment = TextField(
        blank=True,
        null=True,
        max_length=2048,
        help_text="Additional comment(s) on the observation",
    )

    def get_absolute_url(self) -> str:
        return f"/project/{self.proposal.project.pk}/proposal/{self.proposal.pk}/obs/{self.pk}/"

    def get_data_status(self) -> str:
        if not hasattr(self, "dataset"):
            return "Missing"
        elif not self.dataset.is_valid:
            return "Validating"
        elif not self.dataset.radial_velocity:
            return "Acquired"
        elif not self.dataset.arxiv_url and not self.dataset.ads_url:
            return "Analysed"
        else:
            return "Published"

    def get_jd_or_placeholder(self) -> str:
        if self.jd:
            return str(self.jd)
        return '[No date provided]'


User = get_user_model()


@predicate
def is_linked_project_member(user: User, observation: Observation) -> bool:
    """
    Does this user account correspond to a researcher who is a member of the project linked to this observation?

    :param user: User to check.
    :param observation: The Observation to check.
    :return: True if the user is a Researcher who is a member of this observation's linked project, else False.
    """
    return (
        user
        and (user.researcher == observation.proposal.project.principal_investigator)
        or (user.researcher in observation.proposal.project.members.all())
    )


# Rules for database interactions with this source
# Conditions are tested on the user wanting to make the change
add_perm("app.add_observation", is_active)
add_perm("app.change_observation", is_linked_project_member | is_staff)
add_perm("app.delete_observation", is_staff)
add_perm("app.view_observation", is_active)
