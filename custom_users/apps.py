from django.apps import AppConfig


class CustomUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_users'
    
    def ready(self):
        import custom_users.signals 
