from Double_MA import TestStrategy
import time
import backtrader as bt
import backtrader.analyzers as btanalyzers
import pandas as pd
import numpy as np
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import logging

def my_run(arg):

    dataframe = pd.read_csv('xbtusd_data_201701-201712.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe',timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')
    cerebro.addstrategy(TestStrategy, *arg)
    threats=cerebro.run()
    logging.basicConfig(filename='buy_2017_results.log', level=logging.DEBUG)

    final_value = cerebro.broker.getvalue()
    sharp = threats[0].analyzers.mysharpe.get_analysis()['sharperatio']
    drawdown = threats[0].analyzers.mydrawdown.get_analysis().max.drawdown

    out_message = '%s,%s,%s,%s,%s,%.2f,%s,%s,%s' % (arg[0],arg[1], arg[2], arg[4], arg[6],final_value,sharp,drawdown,1)
    print(out_message)
    logging.info(out_message)


def my_run2(arg):

    dataframe = pd.read_csv('xbtusd_data_201801-201812.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy, *arg)
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe',timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')
    cerebro.run()
    logging.basicConfig(filename='MovingAverage_buy_2018_results.log', level=logging.DEBUG)

    final_value = cerebro.broker.getvalue()
    sharp = cerebro.run()[0].analyzers.mysharpe.get_analysis()['sharperatio']
    drawdown = cerebro.run()[0].analyzers.mydrawdown.get_analysis().max.drawdown

    out_message = '%s,%s,%s,%s,%s,%.2f,%s,%s,%s' % (arg[0], arg[1], arg[2], arg[4], arg[6],final_value,sharp,drawdown,1)
    print(out_message)
    logging.info(out_message)


if __name__ == '__main__':
    start = time.time()
    pool = ProcessPoolExecutor(max_workers=38)
    logging.info('begin')

    start = time.time()
    period_long = 15
    period_short = 3
    threshold = 2
    trail_percentage = 0.01
    back_stop_order_percentage = 1.01
    params = []

    for period_long in range(15,1440,360):
        for period_short in range(3,period_long,180):
            for threshold in range(2,50,8):
                for trail_percentage in np.arange(0.01,0.06,0.02):
                    for back_stop_order_percentage in np.arange(1.01,1.06,0.02):
                        params.append([period_short,period_long,threshold,threshold,trail_percentage,trail_percentage,back_stop_order_percentage,back_stop_order_percentage])



    print(params)
    pool.map(my_run, params)
    logging.info('1.log')
    '''pool.map(my_run2, params)
    logging.info('2.log')
    pool.map(my_run3, params)
    logging.info('3.log')
    pool.map(my_run4, params)
    logging.info('4.log')'''


    pool.shutdown(wait=True)
    print(time.time() - start)
