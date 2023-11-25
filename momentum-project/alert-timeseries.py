import datetime
import yfinance as yf
import numpy as np
import time
from slack_sdk.webhook import WebhookClient

url = "https://hooks.slack.com/services/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"
webhook = WebhookClient(url)

CRYPTO = "BTC"
WINDOW = 1

response = webhook.send(text=f"Starting {CRYPTO} trading bot!")

def strategy(df, window=1):
    # Copy the DF
    df = df.copy()
    # Gets the percent change of the holdings
    df["ret"] = np.log(df.Close.pct_change() + 1)
    # Gets the rolling (based on window) returns
    df["prior_n"] = df.ret.rolling(window).sum()
    # Drops NA columns (aka columns without data)
    df.dropna(inplace=True)
    # Determins wether we are calling or shorting
    df["position"] = [1 if i > 0 else 0 for i in df.prior_n]

    df["strat"] = df.position.shift(1) * df.ret
    return df

is_holding = False
balance = 10.00
buy_price = 0

while True:
    today = str(datetime.date.today())
    
    try:
        df1 = yf.download(f"{CRYPTO}-USD", start=today, interval='1m')

        results = strategy(df1)
        last_two_rows = results.tail(2)
        prev, curr = last_two_rows["position"].to_list()
        last_price = last_two_rows.iloc[1].Close

        if not is_holding and prev == 0 and curr == 1:
            # Buy
            buy_price = last_price
            webhook.send(text=f"Buying {CRYPTO} @ ${last_price}")
            is_holding = True
        if is_holding and prev == 1 and curr == 0:
            # Sell
            ret = (last_price - buy_price) / buy_price
            webhook.send(text=f"Selling {CRYPTO} @ ${last_price} for a return of {ret}%")
            is_holding = False

    except Exception as e:
        print(e)
    time.sleep(60)