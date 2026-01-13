from django.urls import path
from .views import RebalancePortfolioView

urlpatterns = [
    path("portfolio/<int:portfolio_id>/rebalance/", RebalancePortfolioView.as_view()),
]
