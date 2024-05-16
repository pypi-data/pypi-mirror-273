from bpx.public import Public

default_public: Public = Public()


def get_volume(filled_orders: list[dict]) -> float | int:
    """
    Return the volume of the filled orders.
    filled_orders is bpx.account.Account.get_fill_history_query() response
    """
    prices = [float(item['price']) * float(item["quantity"]) for item in filled_orders]
    return sum(prices)


def get_fees(filled_orders: list[dict]) -> float | int:
    """
    Return the fees of the filled orders.
    filled_orders is bpx.account.Account.get_fill_history_query() response
    """
    fees = [float(item['price']) * float(item["fee"])
            if item["feeSymbol"] != 'USDC' else float(item["fee"]) for item in filled_orders]
    return sum(fees)


def get_approximate_balance_in_usdc(balance: dict,
                                    time_interval: str = "1m",
                                    public: Public = default_public) -> float:
    """
    Return the approximate account balance in USDC
    balance is bpx.account.Account.get_balances() response
    time_interval is approximate price in USDC in interval(see enums)
    """
    usdc_symbol = "USDC"
    balance_usdc = 0
    close_price = 0
    for symbol in balance:
        if symbol != usdc_symbol:
            k_lines = public.get_klines(f"{symbol}_{usdc_symbol}", time_interval)
            close_price = float(k_lines[-1]['close'])

        for status in balance[symbol]:
            if symbol == usdc_symbol:
                balance_usdc += float(balance[symbol][status])
            else:
                balance_usdc += float(balance[symbol][status]) * close_price
    return balance_usdc
