from django.apps import AppConfig
from iommi import register_search_fields
from iommi.path import register_path_decoding


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
    verbose_name = "Core"
    default = True

    def ready(self):
        from app.models import (
            Cat,
            Owner,
        )

        register_search_fields(model=Cat, search_fields=["name"], allow_non_unique=True)
        register_search_fields(model=Owner, search_fields=["name"], allow_non_unique=True)
        register_path_decoding(cat=Cat)
        register_path_decoding(owner=Owner)

        from app.rules import register_rules

        register_rules()
