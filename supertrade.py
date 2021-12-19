#!/usr/bin/python3

import getopt, sys
import ccxt
import config
import pandas as pd
import numpy as np
import pprint
from datetime import datetime
import time
import crypta 

pair = 'ETH/USDT'
qty = 1.5
timeframe = '5m'
run_interval = 180
LIMIT=300
fee = 0
cost = 1
exchange_name = 'kucoin'

in_position = False
dry_run = False
sale_price = 1000000

def run_bot():
    #print(f"Fetching new bars for {datetime.now().isoformat()}")
    global in_position
    global sale_price
    global fee
    global cost

    exchange = eval("ccxt.%s(%s)" % (exchange_name, config.exchange_keys[exchange_name]))
    
    try:
        bars = exchange.fetch_ohlcv(pair, timeframe=timeframe, limit=LIMIT)
    except ccxt.NetworkError as e:
        print(exchange.id, 'fetch candle failed due to a network error:', str(e))
        return
    except ccxt.ExchangeError as e:
        print(exchange.id, 'fetch candle failed due to exchange error:', str(e))
        return
    except Exception as e:
        print(exchange.id, 'fetch candle failed due to exchange error:', str(e))
        return
    
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    #df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['timestamp'] = pd.to_datetime(df.timestamp, unit = 'ms', utc = True).dt.tz_convert('US/Eastern')
    
    long_term_uptrend = crypta.check_long_uptrend(df, -1)
    short_term_uptrend = crypta.check_short_uptrend(df, -1)

    if in_position:
        if not dry_run and short_term_uptrend < 0:   
            if exchange.has['createMarketOrder']:
                 order = exchange.create_market_sell_order(pair, qty)
                 in_position = False
                 sale_price = float(df.close.iloc[-1])
                 print(order)
            elif exchange.has['createLimitOrder']:
                 # make price a little lower than close price to make sure order is filled
                 order = exchange.create_limit_sell_order(pair, amount = qty - fee, price = df.close.iloc[-1] * 0.95)
                 in_position = False
                 sale_price = float(df.close.iloc[-1])
                 pprint.pprint(order)
                 trade_return = (float(order['info']['filled_total']) - float(order['info']['fee']) - cost) / cost
                 print("-" * 100)
                 print(f"Trade return {trade_return * 100}%")
                 print("-" * 100)
            else:
                print("exchange doesn't have market or limit order")
  
        else:
            print("-" * 100)
            print(f"{pair}@{exchange_name} * {qty - fee} : In position. long term uptrend {'Yes' if long_term_uptrend > 0 else 'No'}; short term trend {'Yes' if short_term_uptrend > 0 else 'No'}")
            print("-" * 100)
    else:
        if not dry_run and long_term_uptrend > 0 and short_term_uptrend > 0:
        #if short_term_uptrend > 0 and df.iloc[-1].close < sale_price and not dry_run: 
            if exchange.has['createMarketOrder']:
                order = exchange.create_market_buy_order(pair, qty)
                in_position = True
                print(order)
            elif exchange.has['createLimitOrder']:
                # make price a little higher than close price to make sure order is filled
                order = exchange.create_limit_buy_order(pair, amount = qty, price = df.close.iloc[-1] * 1.05)
                in_position = True
                fee = float(order['info']['fee'])
                cost = float(order['cost'])
                print("-" * 100)
                pprint.pprint(order)
            else:
                print("exchange doesn't have market or limit order")
        else:
            print(f"{pair}@{exchange_name} * {qty - fee} : Not in position. Sale price {sale_price}; long term uptrend {'Yes' if long_term_uptrend > 0 else 'No'}; short term trend {'Yes' if short_term_uptrend > 0 else 'No'}")
  
    print("-" * 100)
    print(df.tail(3))
    print("-" * 100)

def usage():
    message = """usage: %s [-h|-i|-o|-r|-t|-x|-v] [--help|--in-position|--out-of-position|--timeframe=|--run-every=|--exchange|--dry-run] COIN QUANTITY
        -h, --help: print this help message
        -i, --in-position: run as in position
        -o, --out-of-position: run as out of position
        -t, --timeframe: Candle timeframe, e.g. 1m, 5m, 15m, 30m, 1h, 4h, 1d
        -x, --exchange: exchange name, e.g. binance, gateio, kucoin
        -v, --verbose 
        """ % sys.argv[0]

    print(message)


def main():
    global exchange_name, qty, pair, in_position, timeframe, run_interval, dry_run
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hior:t:x:v", ["help", "in-position", "out-of-position", "timeframe=", "run-every=", "exchange=", "dry-run"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--in"):
            in_position = True
        elif o in ("-o", "--out"):
            in_position = False
        elif o in ("-t", "--timeframe"):
            if a[-1] in ['d', 'h', 'm']:
                timeframe = a
            else:
                print("Timeframe not specified correctly")
                exit(1)
        elif o in ("-x", "--exchange"):
            for key in config.exchange_keys: 
                if key.startswith(a.lower()):
                    exchange_name = key
                    break
            if not exchange_name:
                assert False, "No valid exchange name provided"
        elif o in ("-d", "--dry-run"):
            dry_run = True
        elif o in ("-r", "--run-every"):
            run_interval = int(a)
        else:
            assert False, "unhandled option"

    if len(args) > 2:
        assert False, "There are %s arguments provided. Only two are allowed" % len(args)
    else:
        for arg in args:
            try:
                qty = float(arg)  
            except ValueError:
                pair = arg.upper() + "/USDT"

    order_template ="""
        Exchange: {exchange}
	Pair: {pair}
	Quantity: {quantity}
	In position: {in_position}
	Candle timeframe: {timeframe}
	Run interval: {run_interval} seconds
        """
    trade_specs = order_template.format(exchange = exchange_name, pair = pair, quantity = qty, in_position = in_position, timeframe = timeframe, run_interval = run_interval)
    print(trade_specs)

    accept = input("Trade specifications all correct(Y/n)? ")
    if accept.strip().lower() in ["", "y", "yes"]:
      while True:
         run_bot()
         time.sleep(run_interval)
    elif accept.strip().lower() in ["n", "no"]:
         exit(0)
    else:
         print("Answer not acceptable")
         exit(1)

if __name__ == "__main__":
    main()
