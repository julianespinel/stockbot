# Bot commands

The bot supports the following commands:

1. `/start` - show the description of what the bot can do
2. `/help` - show the list of commands the bot supports
3. `/price {symbol}` - get price stats
4. `/return {symbol}` - get return stats
5. `/vol {symbol}` - get volatility stats
6. `/all {symbol}` - get price, return, and volatility stats

## 1. Start `/start`

### Description

Show the description of what the bot can do.

### Response

```text
I compute statistics about prices, returns and volatility from stocks, ETFs and REITs.
I get the data from Yahoo Finance.

/help will show the list of supported commands.
```

## 2. Help `/help`

### Description

Show the list of commands the bot supports.

### Response

```text
I support the following commands:

/start - show the description of what I can do
/help - show the list of commands I support
/price {symbol} - get price stats
/return {symbol} - get return stats
/vol {symbol} - get volatility stats
/all {symbol} - get price, return, and volatility stats
```

## 3. Price `/price {symbol}`

### Description

Given a stock/ETF symbol, shows price statistics about the given symbol.

The bot will compute and return the following statistics:

- min price: minimum closing price of the symbol in a time range.
- max price: maximum closing price of the symbol in a time range.
- min-max price diff: percentage difference between min price and max price in a time range.
- max negative 1-day change: maximum 1-day difference in which the price decreased in a time range.
- max positive 1-day change: maximum 1-day difference in which the price increased in a time range.

These statistics will be calculated in the following time ranges:
1 month, 3 months, 6 months, 12 months.

### Response

For example, given the command: `/price googl`, it will return:

```text
The price of GOOGL is:

Current price:
98.74 (2022-09-23)

Stats:

1mo
min price: 98.74 (2022-09-23)
max price: 116.65 (2022-08-25)
min-max price diff: -15.35%
max negative 1-day change: -5.90%
max positive 1-day change: 2.60%
---
3mo
min price: 98.74 (2022-09-23)
max price: 122.08 (2022-08-15)
min-max price diff: -19.12%
max negative 1-day change: -5.90%
max positive 1-day change: 7.66%
---
6mo
min price: 98.74 (2022-09-23)
max price: 142.97 (2022-04-04)
min-max price diff: -30.94%
max negative 1-day change: -5.90%
max positive 1-day change: 7.66%
---
12mo
min price: 98.74 (2022-09-23)
max price: 149.84 (2021-11-18)
min-max price diff: -34.10%
max negative 1-day change: -5.90%
max positive 1-day change: 7.66%
---
```

## 4. Return `/return {symbol}`

### Description

Given a stock/ETF symbol, shows return statistics about the given symbol.

The bot will compute and return the following statistics:

- 1mo: percentage return between the today's price and the price 1 month ago.
- 3mo: percentage return between the today's price and the price 3 months ago.
- 6mo: percentage return between the today's price and the price 6 months ago.
- 12mo: percentage return between the today's price and the price 12 months ago.

### Response

For example, given the command: `/return googl`, it will return:

```text
The return of GOOGL is:

Current price:
98.74 (2022-09-23)

Stats:

1mo: -13.15%
3mo: -14.76%
6mo: -30.30%
12mo: -30.57%
```

## 5. Volatility `/vol {symbol}`

### Description

Given a stock/ETF symbol, shows volatility statistics about the given symbol.

The bot will compute and return the following statistics:

- 1mo: volatility of the closing price of the symbol in the last month.
- 3mo: volatility of the closing price of the symbol in the last 3 months.
- 6mo: volatility of the closing price of the symbol in the last 6 months.
- 12mo: volatility of the closing price of the symbol in the last 12 months.

### Response

For example, given the command: `/vol googl`, it will return:

```text
The volatility of GOOGL is:

Current price:
98.74 (2022-09-23)

Stats:

1mo: 10.14%
3mo: 18.46%
6mo: 27.14%
12mo: 34.65%
```

## 6. All `/all {symbol}`

### Description

Given a stock/ETF symbol, shows price, return and volatility statistics about 
the given symbol in the following time ranges: 1 month, 3 months, 6 months,
12 months.

### Response

For example, given the command: `/all googl`, it will return:

```text
The stats of GOOGL are:

Current price:
98.74 (2022-09-23)

Stats:

1mo
min price: 98.74 (2022-09-23)
max price: 116.65 (2022-08-25)
min-max price diff: -15.35%
max negative 1-day change: -5.90%
max positive 1-day change: 2.60%
return: -13.15%
volatility: 10.14%
---
3mo
min price: 98.74 (2022-09-23)
max price: 122.08 (2022-08-15)
min-max price diff: -19.12%
max negative 1-day change: -5.90%
max positive 1-day change: 7.66%
return: -14.76%
volatility: 18.46%
---
6mo
min price: 98.74 (2022-09-23)
max price: 142.97 (2022-04-04)
min-max price diff: -30.94%
max negative 1-day change: -5.90%
max positive 1-day change: 7.66%
return: -30.30%
volatility: 27.14%
---
12mo
min price: 98.74 (2022-09-23)
max price: 149.84 (2021-11-18)
min-max price diff: -34.10%
max negative 1-day change: -5.90%
max positive 1-day change: 7.66%
return: -30.57%
volatility: 34.65%
---
```
