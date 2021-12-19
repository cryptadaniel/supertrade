import pandas_ta as ta

class Supertrend:
    def __init__(self, df, length, multiplier):
        self.length = length
        self.multiplier = multiplier
        self.data = ta.supertrend(high=df['high'], low=df['low'], close=df['close'], length=length, multiplier=multiplier)

    def current_uptrend(self):
        return self.data.iloc[-1, 1]

    def previous_uptrend(self):
        return self.data.iloc[-2, 1]

    def get_uptrend(self, row):
        return self.data.iloc[row, 1]

def above_dema(df, row):
    df.ta.dema(close = 'close', length = 200, append = True)
    if df['close'].iloc[row] >= df['DEMA_200'].iloc[row]:
        #print("DEMA signal buy")
        return df['close'].iloc[row] - df['DEMA_200'].iloc[row]
    else:
        return df['close'].iloc[row] - df['DEMA_200'].iloc[row]

def check_stochrsi(df, row):
    df.ta.stochrsi(high = 'high', low = 'low', close = 'close', append = True)

    if df['STOCHRSId_14_14_3_3'].iloc[row] <= 20:
        #print("Stochrsi signal buy")
        return 1
    elif df['STOCHRSId_14_14_3_3'].iloc[row] >= 80:
        return -1
    else:
        return 0

def check_current_supertrends(df):
    trend_10_1 = Supertrend(df, 10, 1) 
    trend_11_2 = Supertrend(df, 11, 2) 
    trend_12_3 = Supertrend(df, 12, 3) 
    total_current_uptrend = trend_10_1.current_uptrend() + trend_11_2.current_uptrend() + trend_12_3.current_uptrend()
    return total_current_uptrend 

def check_supertrends(df, row):
    trend_10_1 = Supertrend(df, 10, 1) 
    trend_11_2 = Supertrend(df, 11, 2) 
    trend_12_3 = Supertrend(df, 12, 3) 
    total_current_uptrend = trend_10_1.get_uptrend(row) + trend_11_2.get_uptrend(row) + trend_12_3.get_uptrend(row)
    return total_current_uptrend 

def check_long_uptrend(df, row):
    trend_20_5 = Supertrend(df, 20, 5) 
    return trend_20_5.get_uptrend(row)

def check_short_uptrend(df, row):
    trend_10_3 = Supertrend(df, 10, 3) 
    return trend_10_3.get_uptrend(row)

def check_short_trend_buy_signal(df, row):
    trend_10_3 = Supertrend(df, 10, 3) 
    return trend_10_3.get_uptrend(row) > trend_10_3.get_uptrend(row - 1)

def check_suptertrend(df, row):
    trend_10_3 = Supertrend(df, 10, 3) 
    return trend_10_3.get_uptrend(row)

def in_squeeze(df):
    return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

def set_ttm_squeeze(df):

    df['20sma'] = df['close'].rolling(window=20).mean()
    df['stddev'] = df['close'].rolling(window=20).std()
    df['lower_band'] = df['20sma'] - (2 * df['stddev'])
    df['upper_band'] = df['20sma'] + (2 * df['stddev'])

    df['ATR'] = df.ta.atr(high = 'high', low = 'low', close = 'close', length = 20)
    df['lower_keltner'] = df['20sma'] - (df['ATR'] * 1.5)
    df['upper_keltner'] = df['20sma'] + (df['ATR'] * 1.5)

    df['squeeze_on'] = df.apply(in_squeeze, axis=1)
