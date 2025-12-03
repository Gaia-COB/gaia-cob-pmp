"""
Submenu for items relating to projects.
"""


from iommi import LAST
from iommi.main_menu import M

from app.forms.project import ProjectForm
from app.forms.proposal import ProposalForm
from app.main_menu.proposal import proposal_submenu
from app.pages.project import ProjectViewPage
from app.tables.project import ProjectTable

project_submenu: M = M(
    icon="diagram-project",
    include=lambda user, **_: user.is_authenticated and user.is_active,
    view=ProjectTable().as_view(),
    items=dict(
        add=M(
            icon="plus",
            include=lambda user, **_: user.has_perm("app.add_project"),
            view=ProjectForm.create(
                fields=dict(
                    is_valid=dict(
                        after=LAST,
                        initial=lambda user, **_: user.is_staff,
                        editable=False,
                    ),
                    principal_investigator=dict(
                        initial=lambda user, **_: user.researcher,
                    ),
                ),
            ),
        ),
        view=M(
            display_name=lambda project, **_: str(project),
            path="<project>/",
            params={"project"},
            include=lambda user, project, **_: user.has_perm("app.view_project", project),
            url=lambda project, **_: project.get_absolute_url(),
            view=ProjectViewPage().as_view(),
            items=dict(

                change=M(
                    icon="pencil",
                    include=lambda user, project, **_: user.has_perm("app.change_project", project),
                    view=ProjectForm.edit(
                        title=lambda project, **_: f"Change Project \"{project}\"",
                        auto__exclude=["is_valid"],
                        instance=lambda project, **_: project,
                        extra__redirect_to=lambda project, **_: project.get_absolute_url(),
                    ),
                ),
                delete=M(
                    display_name=lambda project, **_: f"Delete Project \"{project}\"",
                    icon="trash",
                    include=lambda user, project, **_: user.has_perm("app.delete_project", project),
                    view=ProjectForm.delete(instance=lambda project, **_: project),
                ),
                add_proposal=M(
                    icon="plus",
                    include=lambda user, project, **_: user.has_perm("app.change_project", project),
                    view=ProposalForm.create(
                        fields=dict(
                            project=dict(
                                initial=lambda project, **_: project,
                                editable=False,
                            ),
                        ),
                    ),
                ),
                view=proposal_submenu,
            ),
        ),
    ),
)
