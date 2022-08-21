from analyze import PriceStats, ReturnStats
from common_types import Period


def human_readable_prices(price_stats: dict[Period, PriceStats]) -> str:
    result = ''
    for period, stats in price_stats.items():
        result += f'{period}\n'
        result += f'min price: {as_decimal(stats.min_price.value)} ({stats.min_price.date})\n'
        result += f'max price: {as_decimal(stats.max_price.value)} ({stats.max_price.date})\n'
        result += f'min-max price diff: {as_percentage(stats.min_price_max_price_difference)}\n'
        result += f'max negative change: {as_percentage(stats.max_negative_change)}\n'
        result += f'max positive change: {as_percentage(stats.max_positive_change)}\n'
        result += '---\n'

    return result


def human_readable_returns(return_stats: ReturnStats) -> str:
    return (
        f'{Period.MONTH}: {as_percentage(return_stats.month)}\n'
        f'{Period.QUARTER}: {as_percentage(return_stats.quarter)}\n'
        f'{Period.HALF}: {as_percentage(return_stats.half)}\n'
        f'{Period.YEAR}: {as_percentage(return_stats.year)}\n'
        '---\n'
    )


def as_percentage(value: float) -> str:
    return f'{as_decimal(value * 100)}%'


def as_decimal(value: float) -> str:
    return '{:.2f}'.format(value)
