#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import datetime
from datetime import date,timedelta
import json
import matplotlib.pyplot as plt
import math
import seaborn as sns
import streamlit as st
from wordcloud import WordCloud
import warnings 
import pymongo
import dns
import yfinance as yf



# In[4]:



          

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
    
    print(net)
    
netreturns()   

client = pymongo.MongoClient("mongodb+srv://adder:wVfhac5c@cluster0.osfgk.mongodb.net/toptickerbot?retryWrites=true&w=majority")
db = client.test
collection_tickers = db['bot_entries']
with open("volumedict.json","r") as read_file:
    volumedict = json.load(read_file)
read_file.close()



collection_tickers.insert_one(volumedict)
client.close()

    

    
 def getdata():
    documents = collection_tickers.find()
    response = {}
    for document in documents:
        response.update(document)
    cache = response.pop('_id')
    df = pd.DataFrame.from_dict(response)
    return df

@st.cache
def wordcloud():
   
    
    with open("wordcloud.json", "r") as read_file:
        tickerdata = json.load(read_file)
    read_file.close()
    
    
    tickerkeys = list(tickerdata.keys())
    wc = WordCloud(background_color="white",width=5000,height=5000, max_words=len(tickerkeys),relative_scaling=0.5,min_font_size=5).generate_from_frequencies(tickerdata)
    plt.axis('off')
    return wc
    
def date():
    s = str(datetime.date.today())+".png" 
    return s


# In[75]:


st.set_page_config( layout='wide')
st.markdown("<h1 style='text-align: center; color: black;'>Top ticker bot- An Accumulation Scanning Bot and Social Media Analyst</h1>", unsafe_allow_html=True)
st.write("Bot that looks for stocks showing accumulation or high explosive potential from price and volume patterns ")
st.write("You can also find financial social media analytics")
st.write("\n")
#st.markdown("<h1 style='text-align: center; color: black;'>Net Return: 43%</h1>", unsafe_allow_html=True)
st.write("current holdings of the bot:")
st.table(getdata())
st.write("positions are updated daily. Follow @toptickerbot on Twitter to get alerts and future updates")
st.write("\n")
col1, col2 =  st.beta_columns(2)
with col1:
    st.title("twitter data analytics ")
    st.write("most talked about 50 S&P 500 tickers and some popular ones:")
    st.image(wordcloud().to_array(),width = 350)
with col2:
    st.title("r/WallStreetBets Scanner")
    st.write("Popularity distribution of popular stocks:")
    st.image('2021-01-26wsb.png', width = 400) 
   
  
# In[ ]:




