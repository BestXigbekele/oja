from django.apps import AppConfig


class NeoshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Neoshop'
    def ready(self):
        import Neoshop.signal
    
