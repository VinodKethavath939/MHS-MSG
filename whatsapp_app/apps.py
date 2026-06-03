"""
Django App Configuration
"""

from django.apps import AppConfig


class WhatsappAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'whatsapp_app'
    verbose_name = 'WhatsApp Notification System'
    
    def ready(self):
        """Run app initialization when Django starts"""
        import logging
        logger = logging.getLogger(__name__)
        logger.info("WhatsApp Notification System loaded")
