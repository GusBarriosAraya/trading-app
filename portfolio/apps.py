from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    """
    App configuration for the portfolio application.

    This class allows Django to identify the app and is the place
    where app-level configuration would live if needed in the future
    (signals, startup logic, etc.).
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "portfolio"
