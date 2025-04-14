from django.apps import AppConfig


class MargaDesignConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.marga_design'
    verbose_name = 'Neva Design'

    def ready(self):
        import apps.marga_design.signals
