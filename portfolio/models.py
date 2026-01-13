from django.db import models

class Stock(models.Model):
    """
    Represents a tradable stock.
    Current price is assumed to be the last available market price.
    """
    symbol = models.CharField(max_length=10, unique=True)
    current_price = models.FloatField()

    def __str__(self):
        return self.symbol


class Portfolio(models.Model):
    """
    A portfolio groups holdings and target allocations.
    """
    name = models.CharField(max_length=100)


class Holding(models.Model):
    """
    Represents how many shares of a stock the portfolio currently owns.
    """
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares = models.IntegerField()


class TargetAllocation(models.Model):
    """
    Target distribution of the portfolio (e.g. 40% META, 60% AAPL).
    Percent is expressed as a number between 0 and 100.
    """
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    percent = models.FloatField()
