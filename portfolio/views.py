from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Portfolio
from .services import PortfolioRebalancer
from .serializers import RebalanceResultSerializer


class RebalancePortfolioView(APIView):
    """
    POST /api/portfolio/<id>/rebalance/

    Returns which stocks to buy or sell to match target allocation.
    """

    def post(self, request, portfolio_id):
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)

        result = PortfolioRebalancer.rebalance(portfolio)
        serializer = RebalanceResultSerializer(result)

        return Response(serializer.data)
