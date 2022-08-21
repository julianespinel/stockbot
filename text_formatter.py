from analyze import PriceStats, AnnualStats, AnnualPriceStats
from common_types import Period


def human_readable_prices(price_stats: AnnualPriceStats) -> str:
    result = _human_readable_price_stats(Period.MONTH, price_stats.month)
    result += '---\n'
    result += _human_readable_price_stats(Period.QUARTER, price_stats.quarter)
    result += '---\n'
    result += _human_readable_price_stats(Period.HALF, price_stats.half)
    result += '---\n'
    result += _human_readable_price_stats(Period.YEAR, price_stats.year)
    result += '---\n'
    return result


def human_readable_annual_stats(annual_stats: AnnualStats) -> str:
    return (
        f'{Period.MONTH}: {as_percentage(annual_stats.month)}\n'
        f'{Period.QUARTER}: {as_percentage(annual_stats.quarter)}\n'
        f'{Period.HALF}: {as_percentage(annual_stats.half)}\n'
        f'{Period.YEAR}: {as_percentage(annual_stats.year)}\n'
    )


def human_readable_all_annual_stats(price_stats: AnnualPriceStats,
                                    return_stats: AnnualStats,
                                    volatility_stats: AnnualStats):
    result = _human_readable_price_stats(Period.MONTH, price_stats.month)
    result += f'return: {as_percentage(return_stats.month)}\n'
    result += f'volatility: {as_percentage(volatility_stats.month)}\n'
    result += '---\n'
    result += _human_readable_price_stats(Period.QUARTER, price_stats.quarter)
    result += f'return: {as_percentage(return_stats.quarter)}\n'
    result += f'volatility: {as_percentage(volatility_stats.quarter)}\n'
    result += '---\n'
    result += _human_readable_price_stats(Period.HALF, price_stats.half)
    result += f'return: {as_percentage(return_stats.half)}\n'
    result += f'volatility: {as_percentage(volatility_stats.half)}\n'
    result += '---\n'
    result += _human_readable_price_stats(Period.YEAR, price_stats.year)
    result += f'return: {as_percentage(return_stats.year)}\n'
    result += f'volatility: {as_percentage(volatility_stats.year)}\n'
    result += '---\n'
    return result


def as_percentage(value: float) -> str:
    return f'{as_decimal(value * 100)}%'


def as_decimal(value: float) -> str:
    return '{:.2f}'.format(value)


# private methods


def _human_readable_price_stats(period: Period, stats: PriceStats):
    return (
        f'{period}\n'
        f'min price: {as_decimal(stats.min_price.value)} ({stats.min_price.date})\n'
        f'max price: {as_decimal(stats.max_price.value)} ({stats.max_price.date})\n'
        f'min-max price diff: {as_percentage(stats.min_price_max_price_difference)}\n'
        f'max negative 1-day change: {as_percentage(stats.max_negative_change)}\n'
        f'max positive 1-day change: {as_percentage(stats.max_positive_change)}\n'
    )
