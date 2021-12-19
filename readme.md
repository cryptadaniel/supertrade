The script waits on two supertrend signals to enter or exit a position. The short term supertrend is the default values of 10 periods and ATR multiplier 3. The long term supertrend is based on 20 periods and ATR multiplier 5. All these can be adjusted in the underlying crypta.py file.

python3 supertrade.py -h to get usage description similar to below:

usage: ./thg.py [-h|-i|-o|-r|-t|-x|-v] [--help|--in-position|--out-of-position|--timeframe=|--run-every=|--exchange] COIN QUANTITY
        -h, --help: print this help message
        -i, --in-position: run as in position
        -o, --out-of-position: run as out of position
        -t, --timeframe: Candle timeframe, e.g. 1m, 5m, 15m, 30m, 1h, 4h, 1d
        -x, --exchange: exchange name, e.g. binance, gateio, kucoin
        -r, --run-interval: interval to run and check close price 
        --dry-run: run script without actually entering or exiting positions
        -v, --verbose 

