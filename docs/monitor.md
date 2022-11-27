# Monitor mode

In monitor mode, the bot execute tasks on a defined schedule.
The tasks supported by monitor mode are:

1. Alert on price anomalies
2. Send portfolio daily report

## 1. Alert on price anomalies

### Description

This task is responsible for verifying if any of the symbols (stocks/ETFs) in
our portfolio have crossed minimum or maximum closing prices in the following
time intervals (in order): 12 months, 6 months, 3 months, 1 month.

If the bot detects that the minimum price for 12 months has been crossed today,
it will notify only about the 12-month limit. The 6-month, 3-month and 1-month
minimum price has also been crossed, but we don't need to send notifications for
them.

This task executes automatically from Monday to Friday at 1800 GMT-5.
(After the US stock market has closed).

### Notification

This is an example of a notification that the symbol `XQQ.TO` has a new 3-month
minimum price:

```text
Price alert for XQQ.TO:
New 3mo Min price: 87.55 (2022-09-23)
Old 3mo values: Min: 87.55 (2022-09-23), Max: 106.05 (2022-08-15)
```

## 2. Send portfolio daily report

This task is responsible for sending a report about the portfolio.

The portfolio is a list of symbols defined by the environment variable
`SYMBOLS`.

The report contains the following information per each symbol in the portfolio:

```text
<symbolN> price: x.xx (current price, float)
1wk: x.xx% (1 week return, percentage)
2wk: x.xx% (2 week return, percentage)
3wk: x.xx% (3 week return, percentage)
1mo: x.xx% (1 month return, percentage)
3mo: x.xx% (3 month return, percentage)
6mo: x.xx% (6 month return, percentage)
12mo: x.xx% (12 month return, percentage)
```

This task executes automatically from Monday to Friday at 1800 GMT-5.
(After the US stock market has closed).

### Notification

This is an example of the report sent to the channel defined by the environment
variable `CHANNEL_ID`.

```text
Portfolio report

XQQ.TO price: 91.63
1wk: 1.65%
2wk: 2.27%
3wk: 11.07%
1mo: 4.20%
3mo: -6.40%
6mo: -6.99%
12mo: -30.78%

... more symbols ...
```
