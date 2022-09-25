# Monitor mode

In monitor mode, the bot execute tasks on a defined schedule.
The tasks supported by monitor mode are:

1. Detect and notify about price anomalies

## 1. Detect and notify about price anomalies

### Description

This task is responsible for verifying if any of the symbols (stocks/ETFs) in
our portfolio have crossed minimum or maximum closing prices in the following
time intervals (in order): 12 months, 6 months, 3 months, 1 month.

If the bot detects that the minimum price for 12 months has been crossed today,
it will notify only about the 12-month limit. The 6-month, 3-month and 1-month
minimum price has also been crossed, but we don't need to send notifications for
them.

This task executes automatically from Monday to Friday at 1800 GMT-4.
(After the US stock market has closed).

### Notification

This is an example of a notification that the symbol `XQQ.TO` has a new 3-month
minimum price:

```text
Price alert for XQQ.TO:
New 3mo Min price: 87.55 (2022-09-23)
Old 3mo values: Min: 87.55 (2022-09-23), Max: 106.05 (2022-08-15)
```
