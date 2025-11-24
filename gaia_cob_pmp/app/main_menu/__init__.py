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

from app.forms.researcher import ResearcherForm
from app.main_menu.researcher import researcher_submenu
from app.main_menu.source import source_submenu
from app.pages import IndexPage, PrivacyPage

main_menu = MainMenu(
    items=dict(
        index=M(
            render=False,
            path="",
            view=IndexPage().as_view(),
        ),
        source=source_submenu,
        researcher=researcher_submenu,
        # This just adds a bar into the menu
        separator_1=M(
            include=lambda user, **_: user.is_authenticated,
            template="app/main_menu/spacer.html",
            view=EXTERNAL,
        ),
        # account_details=M(
        #     icon="user",
        #     include=lambda user, **_: user.is_authenticated,
        #     url="/accounts/"
        # ),
        logout=M(
            icon="right-from-bracket",
            include=lambda user, **_: user.is_authenticated,
            url="/accounts/logout",
            view=EXTERNAL,
        ),
        profile=M(
            icon="user",
            include=lambda user, **_: user.is_authenticated and user.is_active,
            url=lambda user, **_: user.researcher.get_absolute_url(),
            view=ResearcherForm(instance=lambda user, **_: user.researcher).as_view(),
        ),
        iommi_admin=M(
            display_name="Admin",
            icon="lock",
            include=lambda user, **_: user.is_staff,
            paths=Admin.urls().urlpatterns,
            view=Admin.all_models(),
        ),
        separator_2=M(view=EXTERNAL, template="app/main_menu/spacer.html"),
        help=M(
            icon="circle-info",
            url="https://Gaia-COB.github.io/gaia-cob-pmp/",
            view=EXTERNAL,
        ),
        privacy=M(
            icon="lock",
            url="/privacy/",
            view=PrivacyPage().as_view(),
        ),
    ),
)
