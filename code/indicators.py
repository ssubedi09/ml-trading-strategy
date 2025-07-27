import pandas as pd


#author
def author():
    #gatech username
    return "ssubedi33"
#study group
def study_group():
    #No study group
    return "ssubedi33"

def bollinger_bands(df, window_size):
    #simple moving average and standard deviation
    avg = df.rolling(window_size).mean()
    std = df.rolling(window_size).std()
    #upperband and lower band
    upper_band = avg + (2 * std)
    bollinger_band = pd.DataFrame()
    bollinger_band["upper_band"] = upper_band
    lower_band = avg - (2 * std)
    bollinger_band["lower_band"] =  lower_band
    bollinger_band["Average"] = avg
    r = (df - lower_band)/(upper_band - lower_band)
    bollinger_band["r"] = r
    return bollinger_band

def momentum(df, window_size):
    #get momentum
    momentum_ = (df / df.shift(window_size)) - 1
    return momentum_

def macd(df, start_day, end_day):
    #EMA for start and end day
    start = df.ewm(span=start_day).mean()
    end = df.ewm(span=end_day).mean()
    #Moving average convergence divergence
    macd_ = start - end
    # 9 day EMA
    signal_line = macd_.ewm(span=9).mean()
    macd_sig = pd.concat([macd_, signal_line], axis=1)
    macd_sig.columns = ["MACD", "signal"]
    return macd_sig

def golden_death_cross(df, window_size_1, window_size_2):
    avg_1 = df.rolling(window_size_1).mean()
    avg_2 = df.rolling(window_size_2).mean()
    gdc = pd.concat([avg_1, avg_2], axis=1)
    gdc.columns = ["avg_1", "avg_2"]
    return gdc

def rsi(df, window_size):
    #daily_returns
    daily_returns = (df / df.shift(1)) - 1
    daily_returns = daily_returns[1:]

    gain = daily_returns.where(daily_returns > 0, 0)
    loss = abs(daily_returns.where(daily_returns < 0, 0))

    avg_gain = gain.rolling(window=window_size).mean()
    avg_loss = loss.rolling(window=window_size).mean()

    rsi = 100 - (100 / (1 + (avg_gain / avg_loss)))
    rsi_overbought = 70 + avg_gain - avg_gain
    rsi_oversold = 30 + avg_gain - avg_gain
    rsi_ = pd.concat([rsi, rsi_overbought, rsi_oversold], axis=1)
    rsi_.columns = ["rsi", "overbought", "oversold"]
    return rsi_



