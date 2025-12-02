from iommi import Header, Page

from app.forms.project import ProjectForm


class ProjectViewPage(Page):
    """
    The basic view for a project.
    """

    header = Header(lambda project, **_: project)
    detail = ProjectForm(
        auto__exclude=["is_valid"],
        instance=lambda project, **_: project,
        editable=False,
    )
