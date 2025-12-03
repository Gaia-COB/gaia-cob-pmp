"""
Submenu for items relating to projects.
"""

from iommi import Field
from iommi.main_menu import M

from app.forms.observation import DatasetForm, ObservationForm
from app.pages.observation import ObservationViewPage

observation_submenu = M(
    display_name=lambda observation, **_: f"Observation: {observation.source}",
    path="obs/<observation>/",
    params={"observation"},
    include=lambda user, observation, **_: user.has_perm("app.view_observation", observation),
    url=lambda observation, **_: observation.get_absolute_url(),
    view=ObservationViewPage().as_view(),
    items=dict(

        add_dataset=M(
            display_name="Add Dataset",
            icon="plus",
            include=lambda user, observation, **_: not hasattr(observation, "dataset") and user.has_perm("app.change_observation", observation),
            view=DatasetForm.create(
                fields__observation=Field.non_rendered(initial=lambda observation, **_: observation),
                extra__redirect_to=lambda observation, **_: observation.get_absolute_url(),
            ),
        ),
        change_dataset=M(
            display_name="Change Dataset",
            icon="pen-ruler",
            include=lambda user, observation, **_: hasattr(observation, "dataset") and user.has_perm("app.change_observation", observation),
            view=DatasetForm.edit(
                auto__exclude=["observation"],
                instance=lambda observation, **_: observation.dataset,
                extra__redirect_to=lambda observation, **_: observation.get_absolute_url(),
            ),
        ),

        change=M(
            icon="pencil",
            include=lambda user, observation, **_: user.has_perm("app.change_observation", observation),
            view=ObservationForm.edit(
                extra__redirect_to=lambda observation, **_: observation.get_absolute_url(),
                title=lambda **_: "Change Observation",
                instance=lambda observation, **_: observation,
                auto__exclude=['proposal', 'is_valid']
            ),
        ),
        delete=M(
            display_name=lambda **_: "Delete Observation",
            icon="trash",
            include=lambda user, observation, **_: user.has_perm("app.delete_observation", observation),
            view=ObservationForm.delete(instance=lambda observation, **_: observation, extra__redirect_to=lambda observation, **_: observation.proposal.get_absolute_url()),
        ),
    ),
)