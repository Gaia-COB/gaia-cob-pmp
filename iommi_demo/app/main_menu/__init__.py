"""
Main menu that describes the site views and URL structure,
as well as controlling access to the views.

Components can (and should) be broken out into smaller parts in other files.
Putting all the content directly here is just for demo purposes!
"""

from django.template import Template
from iommi import LAST, Column, Form, Header, Page, Table, html
from iommi.admin import Admin
from iommi.main_menu import EXTERNAL, M, MainMenu

from app.main_menu.owners import owners_submenu
from app.models import Cat
from app.pages import HelpPage, PrivacyPage, RankingPage

main_menu = MainMenu(
    items=dict(
        index=M(
            render=False,
            path="",
            view=Page(
                parts=dict(
                    h1=Header("Cat Recorder"),
                    p=html.p("This is a <p> block"),
                    links=html.p(
                        children=dict(
                            h2=Header("Links"),
                            list=html.ul(
                                children=dict(
                                    rspca=html.li(
                                        html.a("RSPCA", attrs__href="https://www.rspca.org.uk"),
                                    ),
                                ),
                            ),
                        )
                    ),
                )
            ).as_view(),
        ),
        rankings=M(
            icon="star",
            view=RankingPage().as_view(),
        ),
        cats=M(
            icon="cat",
            view=Table(
                auto__model=Cat,
                columns=dict(
                    owner=dict(
                        include=lambda user, **_: user.is_authenticated,
                        cell__url=lambda row, **_: row.owner.get_absolute_url(),
                    ),
                    name=dict(
                        cell__url=lambda row, **_: row.get_absolute_url(),
                        filter=dict(
                            include=True,
                            freetext=True,
                        ),
                    ),
                    edit=Column.edit(include=lambda user, **_: user.is_authenticated, after=LAST),
                    delete=Column.delete(include=lambda user, **_: user.is_authenticated, after=LAST),
                ),
            ).as_view(),
            items=dict(
                create=M(
                    icon="plus",
                    include=lambda user, **_: user.is_authenticated,
                    view=Form.create(
                        auto__model=Cat,
                        fields__owner__include=True,  # Relationships not included by default
                    ).as_view(),
                ),
                detail=M(
                    display_name=lambda cat, **_: cat,
                    path="<cat>/",
                    params={"cat"},
                    view=Form(
                        auto=dict(
                            model=Cat,
                            instance=lambda cat, **_: cat,
                        ),
                        editable=False,
                    ).as_view(),
                    url=lambda cat, **_: cat.get_absolute_url(),
                    items=dict(
                        edit=M(
                            icon="pencil",
                            include=lambda user, **_: user.is_authenticated,
                            view=Form.edit(auto__model=Cat, auto__instance=lambda cat, **_: cat).as_view(),
                        ),
                        delete=M(
                            icon="trash",
                            include=lambda user, **_: user.is_authenticated,
                            view=Form.delete(auto__model=Cat, auto__instance=lambda cat, **_: cat).as_view(),
                        ),
                    ),
                ),
            ),
        ),
        owners=owners_submenu,
        # This just adds a bar into the menu
        separator_1=M(view=EXTERNAL, template="main_menu/spacer.html"),
        logout=M(
            icon="right-from-bracket",
            include=lambda user, **_: user.is_authenticated,
            url="/accounts/logout",
            view=EXTERNAL,
        ),
        iommi_admin=M(
            display_name="Admin",
            icon="lock",
            include=lambda user, **_: user.is_staff,
            paths=Admin.urls().urlpatterns,
            view=Admin.all_models(),
        ),
        separator_2=M(view=EXTERNAL, template="main_menu/spacer.html"),
        help=M(
            icon="circle-info",
            url="/help/",
            view=HelpPage().as_view(),
        ),
        privacy=M(
            icon="lock",
            url="/privacy/",
            view=PrivacyPage().as_view(),
        ),
    ),
)
