from decimal import Decimal
from django.db import migrations


def create_initial_data(apps, schema_editor):
    """
    Creates a minimal dataset to test the rebalance endpoint.
    """

    Stock = apps.get_model("portfolio", "Stock")
    Portfolio = apps.get_model("portfolio", "Portfolio")
    Holding = apps.get_model("portfolio", "Holding")
    TargetAllocation = apps.get_model("portfolio", "TargetAllocation")

    # Create stocks
    meta = Stock.objects.create(
        symbol="META",
        current_price=Decimal("300.00")
    )

    aapl = Stock.objects.create(
        symbol="AAPL",
        current_price=Decimal("200.00")
    )

    # Create portfolio
    portfolio = Portfolio.objects.create(
        name="Test Portfolio"
    )

    # Current holdings (intentionally unbalanced)
    Holding.objects.create(
        portfolio=portfolio,
        stock=meta,
        shares=10   # 3000 USD
    )

    Holding.objects.create(
        portfolio=portfolio,
        stock=aapl,
        shares=5    # 1000 USD
    )

    # Target allocation: 40% META, 60% AAPL
    TargetAllocation.objects.create(
        portfolio=portfolio,
        stock=meta,
        percent=40
    )

    TargetAllocation.objects.create(
        portfolio=portfolio,
        stock=aapl,
        percent=60
    )


def reverse_initial_data(apps, schema_editor):
    """
    Removes test data on migration rollback.
    """
    Stock = apps.get_model("portfolio", "Stock")
    Portfolio = apps.get_model("portfolio", "Portfolio")

    Portfolio.objects.filter(name="Test Portfolio").delete()
    Stock.objects.filter(symbol__in=["META", "AAPL"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_initial_data,
            reverse_code=reverse_initial_data
        )
    ]
