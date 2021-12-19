The script waits on two supertrend signals to enter or exit a position. The short term supertrend is the default values of 10 periods and ATR multiplier 3. The long term supertrend is based on 20 periods and ATR multiplier 5. All these can be adjusted in the underlying crypta.py file.

I have used the script to trade on Kucoin, Gateio and Binance for quite a few alt coins with good results on short time frames such as 5m or 3m candles. I often activate it after a reversal to uptrend or when I want to take profits on a coin and use it as trailing stop. Other times I add condition to buy only at a price lower than the last sale price and leave it running for extended time. 

The script is free to use but I am not responsible for any gains or losses it incurs. Use it at your own discretion.

The script requires python3 to run and following modules are needed:

pip3 install pandas
pip3 install pandas-ta
pip3 install ccxt

type 'python3 supertrade.py -h' to get usage description similar to below:

usage: ./supertrade.py [-h|-i|-o|-r|-t|-x|-v] [--help|--in-position|--out-of-position|--timeframe=|--run-every=|--exchange] COIN QUANTITY
        -h, --help: print this help message
        -i, --in-position: run as in position
        -o, --out-of-position: run as out of position
        -t, --timeframe: Candle timeframe, e.g. 1m, 5m, 15m, 30m, 1h, 4h, 1d
        -x, --exchange: exchange name, e.g. binance, gateio, kucoin
        -r, --run-interval: interval to run and check close price 
        --dry-run: run script without actually entering or exiting positions
        -v, --verbose 

