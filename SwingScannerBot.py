#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy
import webbrowser
import time
import pandas as pd
import datetime
from datetime import date,timedelta
import schedule
import requests
import json
import bs4 as bs
import pickle
import matplotlib.pyplot as plt
import math
import os
from json.decoder import JSONDecodeError


# In[54]:


import seaborn as sns
import streamlit as st
from wordcloud import WordCloud
import warnings 


# In[28]:



          

def returns():#RETURNS FOR ALL THE EXISTING POSITIONS STORED IN VOLUMEDICT
    with open("volumedict.json","r") as read_file:
        volumedict = json.load(read_file)
    read_file.close()
    keys = list(volumedict.keys())
    returnsdict = {}

    for i in keys:
        current_stock = fetchstock(i)
        totalchange = ((current_stock['lastPrice'] - volumedict[i]["alertedprice"])/volumedict[i]["alertedprice"])*100
        returnsdict[i] = totalchange
        time.sleep(0.2)
    return returnsdict

def manualEntry(ticker,change):
    with open("totalprofits.json","r") as read_file:
        totalreturns = json.load(read_file)
    read_file.close()
    totalreturns[ticker] = change
    with open("totalprofits.json", "w") as write_file:
        json.dump(totalreturns, write_file,indent = 6, skipkeys = True)
    write_file.close() 
    
def snsbar():
    with open("totalprofits.json","r") as read_file:
        totalreturns = json.load(read_file)
    read_file.close()
    tickers = list(totalreturns.keys())
    changes = list(totalreturns.values())
    fig = sns.barplot(x = changes,y = tickers,orient = 'h')
    plt.xlabel("Return since entry")
    plt.ylabel("Ticker")
    plt.title("Returns from toptickerbot entries this week")
    return fig
    

def netreturns():
    with open("totalprofits.json","r") as read_file:
        totalreturns = json.load(read_file)    
    read_file.close()
    net = 0
    keys = list(totalreturns.keys())
    for i in keys:
        net+=totalreturns[i]
    #totalreturns["netreturn"] = net
    cache = totalreturns.pop("netreturn",None)
    with open("totalprofits.json", "w") as write_file:
        json.dump(totalreturns, write_file,indent = 6, skipkeys = True)
    write_file.close()
    return net
    
    


# In[58]:


def positionstable():
    with open("volumedict.json","r") as read_file:
        volumedict = json.load(read_file)
    read_file.close()
    newdict = {}
    volumekeys = list(volumedict.keys())
    for key in volumekeys:
        tickerdict = {}
        tickerdict["price when alerted"] = volumedict[key]["alertedprice"]
        tickerdict["date when alerted"] = volumedict[key]["entrytime"]
        newdict[key] = tickerdict
        
        
    df = pd.DataFrame.from_dict(newdict)
    return df

def wordcloud():
   
    plt.style.use('fivethirtyeight')
    warnings.filterwarnings('ignore')
    with open("wordcloud.json", "r") as read_file:
        tickerdata = json.load(read_file)
    read_file.close()
    tickerkeys = list(tickerdata.keys())
    wc = WordCloud(background_color="white",width=5000,height=5000, max_words=len(tickerkeys),relative_scaling=0.5,min_font_size=5).generate_from_frequencies(tickerdata)
    plt.axis('off')
    plt.show()


# In[61]:


st.title('Top ticker bot- A Swing Trading Bot and Twitter Analyst')
st.write('Hello!, this is where you can find information for toptickerbot, a swing trading bot that identifies accumulating stocks and provides financial twitter data')
st.write("\n")
st.write("current holdings of the bot:")
st.table(positionstable())
st.write("positions are updated daily. Follow @toptickerbot on Twitter to get alerts and future updates")
st.write("\n")
st.write("Returns for last week: 55%")
st.image('2021-01-16 returns.png')
st.write("\n")
st.write("Returns for this week will be shown here at the end of week")
st.write("\n")
st.title("twitter data analytics ")
st.write("most talked about 50 S&P 500 tickers and some popular ones:")
st.image('2021-01-22.png',width = 400)

#st.write("Check out the returns for toptickerbot this week:")
#snsbar()
#st.pyplot(plt)


# In[ ]:




