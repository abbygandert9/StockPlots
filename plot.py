import numpy as np
import pandas as pd
#import pandas_datareader.data as web
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
stock = 'VTI'
#desired stock ticker
pct = 25
#desired percentage above desired time period low to stay below
start = dt.datetime(2022, 7, 25)
#start date of graph and analysis

def graph(stock, start):
    end = dt.datetime.now()
    data = yf.download(stock, start=start, end=end, threads=False)
    #download all stock data from specified start date to end date
    df = pd.DataFrame(data, columns=['Close'])
    #adding only closing price data to data frame object
    df['200d'] = df['Close'].rolling(200).mean()
    #creating new line with a rolling 200 day average
    df['50d'] = df['Close'].rolling(50).mean()
    #creating new line with a rolling 50 day average
    weeks = round(((end-start).days/7))
    #calculating number of weeks between start and end dates
    plt.title(str(weeks)+ ' week '+ str(stock)+ ' prices')
    plt.xlabel('Date')
    plt.ylabel('Share Price ($)')
    plt.plot(df['Close'], label="Prices")
    plt.plot(df['200d'], label="200 day avg")
    #plotting new 200 day average line
    plt.plot(df['50d'], label="50 day avg")
    #plotting new 50 day average line
    plt.legend()
    plt.show()
    #making plot visible
    #print(df)
    #printing the results of each of the three lines (closing prices, 200d avg, 50d avg
    min=df['Close'].min()
    #finding the minimum of the closing prices column, in dollars
    min_index=df['Close'].idxmin()
    #finding the date of the minimum closing price
    print('Minimum: ', min_index.date(), '$', min)
    max=df['Close'].max()
    #finding the maximum of the closing prices column, in dollars
    max_index=df['Close'].idxmax()
    #finding the date of the maximum closing price
    print('Maximum: ',max_index.date(), '$', max)
    curr=df['Close'].iloc[-1]
    #finding the most recent closing price (sepcified end date)
    print('Current: ',end.date(), '$', curr)
    percent(max, min, curr, pct)
    #call to percent method using new min, max, and curr calculations. Uses desired pct value

def percent(max, min, curr, pct):
    #method that determines the percent increase over the price of the designated time frame
    #e.g. the NDAQ price on 7/25/23 is $51.06, which is only 10% above the 52 week low of $48.97
    calc=((max-min)*(pct/100))+min
    actual=((curr-min)/(max-min))*100
    boo=False
    #set default boolean value to False
    if(curr<calc):
        #checks whether the current price is less than calculated percentage
        boo=True
        #turns boolean to True only when condition has been met
    b = 'Bottom '+ str(pct) + '%: $'+ str(calc)
    #output what the cutoff is to reach the calculated percentage
    c = 'Current: $' + str(curr)
    #output current price
    a = 'Actual: ' + str(actual) + '%'
    #output current percentage above designated time period low
    print('\n',boo,'\n', b, '\n', c, '\n', a)
    return boo, calc, actual

graph(stock, start)
#call to graph method to plot the graph
