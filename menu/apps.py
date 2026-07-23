from django.apps import AppConfig


class MenuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'menu'

    def ready(self):
        from menu.patches import apply_context_copy_patch
        apply_context_copy_patch()
