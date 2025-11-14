"""
Submenu for items relating to cat-owners.
"""

from iommi import LAST, Column, Form, Table
from iommi.main_menu import M

from app.models import Owner

owners_submenu: M = M(
    icon="person-walking",
    view=Table(
        auto__model=Owner,
        columns=dict(
            name=dict(
                cell__url=lambda user, row, **_: row.get_absolute_url_if_permitted(user),
                filter=dict(
                    include=True,
                    freetext=True,
                ),
            ),
            cat_set=dict(
                include=True,
            ),
            edit=Column.edit(include=lambda user, **_: user.is_staff, after=LAST),
            delete=Column.delete(include=lambda user, **_: user.is_staff, after=LAST),
        ),
        query__advanced__include=False,
    ),
    items=dict(
        create=M(
            icon="plus",
            include=lambda user, **_: user.has_perm("app.create_owner"),
            view=Form.create(
                auto__model=Owner,
                instance=lambda owner, **_: owner,
                fields__cat_set=dict(
                    include=True,
                ),
            ),
        ),
        detail=M(
            display_name=lambda owner, **_: owner,
            path="<owner>/",
            params={"owner"},
            include=lambda user, owner, **_: user.has_perm("app.view_owner", owner),
            url=lambda owner, **_: owner.get_absolute_url(),
            view=Form(
                auto__model=Owner,
                instance=lambda owner, **_: owner,
                editable=False,
            ),
            items=dict(
                edit=M(
                    icon="pencil",
                    include=lambda user, owner, **_: user.has_perm("app.edit_owner", owner),
                    view=Form.edit(
                        auto__model=Owner,
                        instance=lambda owner, **_: owner,
                        fields__user=dict(
                            choice_queryset=lambda queryset, user, **_: queryset if user.is_staff else queryset.filter(email=user.email),
                        ),
                    ),
                ),
                delete=M(
                    icon="trash",
                    include=lambda user, owner, **_: user.has_perm("app.delete_owner", owner),
                    view=Form.delete(
                        auto__model=Owner,
                        instance=lambda owner, **_: owner,
                    ),
                ),
            ),
        ),
    ),
)
