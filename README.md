# StockBot

This repository contains the code that powers the Telegram bot: `@bernankebot`.
It is named in "honor" of the FED chairman Ben Bernanke.

The bot supports the following commands:

1. `/start` - show the description of what the bot can do
2. `/help` - show the list of commands the bot support
3. `/price {symbol}` - get price stats
4. `/return {symbol}` - get return stats
5. `/vol {symbol}` - get volatility stats
6. `/all {symbol}` - get price, return, and volatility stats

## Install

1. `virtualenv venv`
2. `source venv/bin/activate`
3. `make install`

## Test

1. `make test`

## Run

1. `make run`

## Maintenance

The code is organized in the following way:

1. We have components, each component has a single responsibility.
2. Each component has its own folder.
3. The folder of each component has its source code and tests.

We have the following components:

1. download: it is responsible for downloading the data we need to perform
   analysis.
2. analyze: it is responsible for performing the analysis over the data.
3. bot: it is responsible for receiving commands and return answers from
   platforms such as Telegram.
4. common: it is responsible to hold common types and data structures.

### Project structure

To visualize the project structure, please execute the following command:

```bash
tree -I 'venv|__pycache__|test_files'
```
