from decimal import Decimal, getcontext, ROUND_FLOOR, ROUND_HALF_UP

getcontext().prec = 28


class PortfolioRebalancer:
    """
    Rebalanceador con:
    - Dinero en Decimal
    - Acciones como ENTEROS positivos
    - Cash remainder explícito
    """

    MONEY_PRECISION = Decimal("0.01")

    @staticmethod
    def rebalance(portfolio):
        holdings = portfolio.holding_set.select_related("stock")
        targets = portfolio.targetallocation_set.select_related("stock")

        total_value = Decimal("0")
        current_shares = {}
        current_values = {}

        # 1. Valor actual del portfolio
        for holding in holdings:
            price = Decimal(str(holding.stock.current_price))
            shares = int(holding.shares)

            value = price * shares
            total_value += value

            current_shares[holding.stock.symbol] = shares
            current_values[holding.stock.symbol] = value

        total_value = total_value.quantize(
            PortfolioRebalancer.MONEY_PRECISION, rounding=ROUND_HALF_UP
        )

        actions = []
        spent_cash = Decimal("0")

        # 2. Rebalanceo según target
        for target in targets:
            symbol = target.stock.symbol
            price = Decimal(str(target.stock.current_price))
            percent = Decimal(str(target.percent)) / Decimal("100")

            target_value = (total_value * percent).quantize(
                PortfolioRebalancer.MONEY_PRECISION, rounding=ROUND_HALF_UP
            )

            current_value = current_values.get(symbol, Decimal("0"))
            delta_value = target_value - current_value

            # 3. Convertir a acciones ENTERAS
            raw_shares = (delta_value / price)

            shares_delta = int(
                raw_shares.to_integral_value(rounding=ROUND_FLOOR)
            )

            if shares_delta == 0:
                continue

            executed_value = price * abs(shares_delta)
            spent_cash += executed_value

            actions.append({
                "stock": symbol,
                "action": "BUY" if shares_delta > 0 else "SELL",
                "shares": abs(shares_delta)
            })

        # 4. Cash no asignado
        cash_remainder = (total_value - spent_cash).quantize(
            PortfolioRebalancer.MONEY_PRECISION, rounding=ROUND_HALF_UP
        )

        return {
            "total_value": total_value,
            "cash_remainder": cash_remainder,
            "actions": actions
        }
