# Candlestick Pattern Generation
Code to generate candlestick pattern.

## How to Run

Command: `python binance_api.py`

## Settings
<ol>
    <li>Platform: Binance</li>
    <li>Ticker: BTCBUSD</li>
    <li>Timeframe: 1D</li>
    <li>Date: 2023-02-08</li>
</ol>

## Prerequisites

1. Installed Python.
2. Installed pip.
3. Has Binance account.

## Steps
1. Obtain Binance API key. https://algotrading101.com/learn/binance-python-api-guide/#:~:text=Obtaining%20an%20API%20key

2. Set API keys as environment variables.

    `set binance_api=your_api_key_here`

    `set binance_secret=your_api_secret_here`     

3. Install python-binance library. 

    `pip install python-binance`

4. Install pandas library.

    `pip install pandas`

5. Install Pillows library.

    `pip install Pillow`

3. Hit Binance API to retrieve historical data.

4. Retrieve candle high, low, open and close; then create a Pandas DataFrame.

5. Generate drawing manually based on candlestick data.

