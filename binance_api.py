from datetime import date
import os
import pandas as pd
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont, ImageOps

from binance import Client

########################################################################################
#
# Setup
#
########################################################################################

api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

client = Client(api_key,api_secret)
client.API_URL = 'https://testnet.binance.vision/api'

ticker = 'BTCBUSD'
timeframe = Client.KLINE_INTERVAL_1DAY

# get timestamp of earliest date data is available
# timestamp = client._get_earliest_valid_timestamp(ticker, timeframe)
timestamp = '2023-02-08'

########################################################################################
#
# Calculation
#
########################################################################################

# request historical candle (or klines) data
bars = client.get_historical_klines(ticker, timeframe, timestamp, limit=1000)

# Sample response data from Binance API documentation. 
# Ref: https://binance-docs.github.io/apidocs/spot/en/#compressed-aggregate-trades-list:~:text=Data%20Source%3A%20Database-,Kline/Candlestick%20Data,-Response%3A
# [
#   [
#     1499040000000,      // Kline open time
#     "0.01634790",       // Open price
#     "0.80000000",       // High price
#     "0.01575800",       // Low price
#     "0.01577100",       // Close price
#     "148976.11427815",  // Volume
#     1499644799999,      // Kline Close time
#     "2434.19055334",    // Quote asset volume
#     308,                // Number of trades
#     "1756.87402397",    // Taker buy base asset volume
#     "28.46694368",      // Taker buy quote asset volume
#     "0"                 // Unused field, ignore.
#   ]
# ]

# delete unwanted data - just keep date, open, high, low, close
for line in bars:
    del line[5:]

# create a Pandas DataFrame
btc_df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])

btc_df['open'] = btc_df['open'].astype(float)
btc_df['high'] = btc_df['high'].astype(float)
btc_df['low'] = btc_df['low'].astype(float)
btc_df['close'] = btc_df['close'].astype(float)
btc_df['date'] = pd.to_datetime(btc_df['date'], unit='ms')
btc_df['difference_pct'] = ((btc_df['close'] - btc_df['open']) / btc_df['close'] * 100)

# btc_df.set_index('date', inplace=True)

# getting only one data for now
btc_df_sample = btc_df[:1]
print(btc_df_sample)

########################################################################################
#
# Drawing
#
########################################################################################

def draw_frame(object, object_type, color):
    x1, y1 = object[2], object[3]
    x2, y2 = object[2] + object[0], object[3] + object[1]

    fill = None
    if object_type == 'body':
        fill = color

    draw.rectangle([x1, y1, x2, y2], outline=color, fill=fill)

# size of image
canvas_width = 2000
canvas_height = 2000
canvas = (canvas_width, canvas_height)
# scale ration
scale = 5
thumb = canvas[0]/scale, canvas[1]/scale

for index, row in btc_df_sample.iterrows():

    # init canvas
    im = Image.new('RGBA', canvas, (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)

    width_mid = canvas_width / 2
    height_mid = canvas_height / 2

    # rectangles (width, height, left position, top position)
    candle_shadow_top = canvas_height / 10
    candle_shadow_left = width_mid
    candle_shadow_width = 1
    candle_shadow_height = canvas_height-candle_shadow_top-candle_shadow_top
    candle_shadow = (candle_shadow_width, candle_shadow_height, candle_shadow_left, candle_shadow_top)

    color = ('green' if row['difference_pct'] > 0 else 'red')

    draw_frame(candle_shadow, 'shadow', color)

    candle_body_width = canvas_width/10
    candle_body_left = width_mid - (candle_body_width / 2)
    price_height = row['high'] - row['low']
    candle_body_top = (row['high'] - row['open']) / price_height * candle_shadow_height
    candle_body_height = (row['open'] - row['close']) / price_height * candle_shadow_height
    candle_body = (candle_body_width, candle_body_height, candle_body_left, candle_body_top)

    draw_frame(candle_body, 'body', color)

    # Custom font style and font size
    myFont = ImageFont.truetype('arial.ttf', 100)

    # open_str = "$" + row['open'] + " \n "
    open_str = "$" + str(row['open']) + " \n\n"
    # change_str = "Change: " + row['difference_pct'].astype(str) + "% \n "
    change_str = "Change: " + str(round(row['difference_pct'], 2)) + "%"
    text = open_str + change_str
    draw.text((width_mid+candle_body_width,height_mid-canvas_height/10), text, font=myFont, fill = color)

    # make thumbnail
    im.thumbnail(thumb)

    file_name = 'C:/Users/User/repo/crpyto/' + ticker + ' ' + row['date'].strftime("%Y-%m-%d") + '.png'

    # save image
    im.save(file_name)

    # Open image
    im = Image.open(file_name)

    # Add border and save
    bordered = ImageOps.expand(im, border=10, fill=color)

    bordered.save(file_name)