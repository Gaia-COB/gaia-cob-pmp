"""
Submenu for items relating to projects.
"""

from django.contrib.auth import get_user_model

from iommi import LAST
from iommi.main_menu import M

from app.forms.project import ProjectForm
from app.forms.proposal import ProposalForm
from app.pages.project import ProjectViewPage
from app.pages.proposal import ProposalViewPage
from app.tables.project import ProjectTable

proposal_submenu = M(
    display_name=lambda proposal, **_: proposal,
    path="proposal/<proposal>/",
    params={"project", "proposal"},
    include=lambda user, proposal, **_: user.has_perm("app.view_proposal", proposal),
    url=lambda proposal, **_: proposal.get_absolute_url(),
    view=ProposalViewPage().as_view(),
    items=dict(
        change=M(
            icon="pencil",
            include=lambda user, proposal, **_: user.has_perm("app.change_proposal", proposal),
            view=ProposalForm.edit(
                extra__redirect_to=lambda proposal, **_: proposal.get_absolute_url(),
                title=lambda project, proposal, **_: f"Change {project}: Proposal {proposal.get_project_index()}",
                instance=lambda proposal, **_: proposal,
                auto__exclude=['project']
            ),
        ),
        delete=M(
            display_name=lambda proposal, **_: f"Delete Proposal {proposal.get_project_index()}",
            icon="trash",
            include=lambda user, proposal, **_: user.has_perm("app.delete_proposal", proposal),
            view=ProposalForm.delete(instance=lambda proposal, **_: proposal, extra__redirect_to=lambda proposal, **_: proposal.project.get_absolute_url()),
        ),
    ),
)