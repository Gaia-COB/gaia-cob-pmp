"""
Submenu for items relating to researchers
"""

from iommi.main_menu import M

from app.forms.researcher import ResearcherForm
from app.tables.researcher import ResearcherTable

researcher_submenu: M = M(
    icon="users",
    include=lambda user, **_: user.is_authenticated and user.is_active,
    view=ResearcherTable(auto__exclude=["orcid"]),
    items=dict(
        view=M(
            display_name=lambda researcher, **_: researcher,
            path="<researcher>/",
            params={"researcher"},
            include=lambda user, researcher, **_: user.has_perm("app.view_researcher", researcher),
            url=lambda researcher, **_: researcher.get_absolute_url(),
            view=ResearcherForm(
                auto__exclude=["user"],
                title=lambda researcher, **_: f"{researcher}",
                instance=lambda researcher, **_: researcher,
                editable=False,
            ).as_view(),
            items=dict(
                change=M(
                    icon="pencil",
                    include=lambda user, researcher, **_: user.has_perm(
                        "app.change_researcher", researcher
                    ),
                    view=ResearcherForm.edit(
                        auto__exclude=["user"],
                        title=lambda researcher, **_: f"Change {researcher}",
                        instance=lambda researcher, **_: researcher,
                    ),
                ),
            ),
        ),
    ),
)
