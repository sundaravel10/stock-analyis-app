
from cmath import log
from importlib.resources import path
from pandas import DataFrame
from pynse import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
from Scripts.src.main import constants
logging.basicConfig(level=logging.INFO,format='%(message)s')

def calculate_52_wk_delta(top_losers_symbols,dateLastYear):
    logging.info('Inside calculate_52_wk_delta')
    resultDf = DataFrame(columns=[constants.CURRENT_STOCK_PRICE,constants.FIFY_TWO_WEEKS_HIGH, constants.DELTA_VALUE,constants.PERCENTAGE_CHANGE])
    for symbol in top_losers_symbols:
        historical_df = nse.get_hist(symbol,from_date=dateLastYear,to_date=datetime.now().date())
        fifty_two_Week_high = (historical_df.sort_values('close',ascending=False))['close'].iloc[0]
        currentValueOfStock = nse.get_quote(symbol)
        fifty_two_Week_delta = currentValueOfStock['lastPrice'] - fifty_two_Week_high
        resultDf.loc[symbol,constants.CURRENT_STOCK_PRICE] =  currentValueOfStock['lastPrice']
        resultDf.loc[symbol,constants.FIFY_TWO_WEEKS_HIGH] = fifty_two_Week_high
        resultDf.loc[symbol,constants.DELTA_VALUE] = fifty_two_Week_delta
        resultDf.loc[symbol,constants.PERCENTAGE_CHANGE] = ((currentValueOfStock['lastPrice'] - fifty_two_Week_high)/currentValueOfStock['lastPrice']) * 100
    return resultDf
    
    

nse = Nse()
top_losers_df_full = nse.top_losers(index=IndexSymbol.Nifty50,length=10)
top_losers = top_losers_df_full[['lastPrice','previousClose','change']]
top_losers_symbols = top_losers.index.tolist()
date = datetime.now() - relativedelta(years=1)
dateLastYear = date.date()
resultDf = calculate_52_wk_delta(top_losers_symbols,dateLastYear)
resultDf = resultDf.sort_values(constants.DELTA_VALUE,ascending=True)
logging.info('Result DataFrame ')
print(resultDf)







