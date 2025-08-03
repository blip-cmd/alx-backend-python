from django.apps import AppConfig


class MessagingConfig(AppConfig):
    """
    Configuration for the messaging app.
    This ensures that Django signals are properly registered when the app is loaded.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'
    verbose_name = 'Messaging System'

    def ready(self):
        """
        Called when Django starts up.
        This method imports the signals module to register all signal handlers.
        """
        import messaging.signals
