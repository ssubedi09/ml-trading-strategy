import datetime as dt
import pandas as pd
from util import get_data
import indicators as ind


class ManualStrategy:
    def __init__(self, verbose=False, impact=0.0, commission=0.0):
        self.verbose = verbose
        self.commission = commission
        self.impact = impact

    def author(self):
        #gatech username
        return "ssubedi33"

    def study_group(self):
        #No study group
        return "ssubedi33"

    def add_evidence(self, symbol="IBM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1),sv=10000):
        pass

    def testPolicy(self, symbol='JPM', sd=dt.datetime(2010, 1, 1, 0, 0), ed=dt.datetime(2011, 12, 31, 0, 0), sv=100000):
        prices_stock = get_data([symbol], pd.date_range(sd, ed))
        prices_stock = prices_stock.dropna()
        prices_stock = prices_stock/prices_stock.iloc[0]
        bb = ind.bollinger_bands(prices_stock[symbol], 25)
        m = ind.momentum(prices_stock[symbol], 25)
        rsi = ind.rsi(prices_stock[symbol], 25)
        df_signal = pd.DataFrame(index=prices_stock.index, columns=["Symbol", "Order","Shares"])
        prev_trans = 0
        df_signal.iloc[0] = [symbol, "HOLD", 0]
        buy = []
        sell = []
        for i in range(len(df_signal)-1):
            if rsi.iloc[i]["rsi"] < 30 or bb.iloc[i]['r'] < 0 or m.iloc[i] < -0.2:
                # check current holdings
                if prev_trans == 0:
                    df_signal.iloc[i+1] = [symbol, "BUY", 1000]
                    prev_trans = 1
                    buy.append(df_signal.index[i+1])
                elif prev_trans == -1:
                    df_signal.iloc[i+1] = [symbol, "BUY", 2000]
                    prev_trans = 1
                    buy.append(df_signal.index[i + 1])
                else:
                    df_signal.iloc[i + 1] = [symbol, "HOLD", 0]
            elif rsi.iloc[i]["rsi"] > 70 or bb.iloc[i]['r'] > 1 or m.iloc[i] > 0.2:
                # check current holdings
                if prev_trans == 0:
                    df_signal.iloc[i+1] = [symbol, "SELL", 1000]
                    sell.append(df_signal.index[i + 1])
                    prev_trans = -1
                elif prev_trans == 1:
                    df_signal.iloc[i+1] = [symbol, "SELL", 2000]
                    prev_trans = -1
                    sell.append(df_signal.index[i + 1])
                else:
                    df_signal.iloc[i + 1] = [symbol, "HOLD", 0]
            else:
                df_signal.iloc[i+1] = [symbol, "HOLD", 0]
        #Final
        if prev_trans == -1:
            df_signal.iloc[-1] = [symbol, "BUY", 1000]
            buy.append(df_signal.index[-1])
        elif prev_trans == 1:
            df_signal.iloc[-1] = [symbol, "SELL", 1000]
            sell.append(df_signal.index[-1])

        return df_signal, buy, sell
