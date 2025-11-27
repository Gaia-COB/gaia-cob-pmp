"""
Submenu for items relating to sources.
"""

from iommi import LAST, Field
from iommi.main_menu import M

from app.forms.source import SourceForm, SourceGaiaInfoForm
from app.pages.source import SourceViewPage
from app.tables.source import SourceTable

source_submenu: M = M(
    icon="sun",
    include=lambda user, **_: user.is_authenticated and user.is_active,
    view=SourceTable().as_view(),
    items=dict(
        add=M(
            icon="plus",
            include=lambda user, **_: user.has_perm("app.add_source"),
            view=SourceForm.create(
                fields=dict(
                    is_active=dict(
                        # We could exclude this (with `auto__exclude=['is_active']`) but we don't to show the users.
                        after=LAST,
                        initial=lambda user, **_: user.is_staff,
                        editable=False,
                    )
                ),
            ),
        ),
        view=M(
            display_name=lambda source, **_: source,
            path="<source>/",
            params={"source"},
            include=lambda user, source, **_: user.has_perm("app.view_source", source),
            url=lambda source, **_: source.get_absolute_url(),
            view=SourceViewPage().as_view(),
            items=dict(
                # Adds the source Gaia info, with the source defaulting to the current one
                add_gaiainfo=M(
                    display_name=lambda source, **_: f"Add {source} Gaia info",
                    icon="plus",
                    include=lambda user, source, **_: not hasattr(source, "gaiainfo")
                    and user.has_perm("app.add_sourcegaiainfo"),
                    view=SourceGaiaInfoForm.create(
                        fields__source=Field.non_rendered(initial=lambda source, **_: source),
                    ),
                ),
                change=M(
                    icon="pencil",
                    include=lambda user, source, **_: user.has_perm("app.change_source", source),
                    view=SourceForm.edit(
                        title=lambda source, **_: f"Change {source}",
                        auto__exclude=["is_active"],
                        instance=lambda source, **_: source,
                    ),
                ),
                change_gaiainfo=M(
                    display_name=lambda user, source, **_: f"Change {source} Gaia info",
                    icon="pen-ruler",
                    include=lambda user, source, **_: hasattr(source, "gaiainfo")
                    and user.has_perm("app.change_sourcegaiainfo"),
                    view=SourceGaiaInfoForm.edit(
                        auto__exclude=["is_active", "source"],
                        instance=lambda source, **_: source.gaiainfo,
                    ),
                ),
                delete=M(
                    display_name=lambda source, **_: f"Delete {source}",
                    icon="trash",
                    include=lambda user, source, **_: user.has_perm("app.delete_source", source),
                    view=SourceForm.delete(instance=lambda source, **_: source),
                ),
            ),
        ),
    ),
)
