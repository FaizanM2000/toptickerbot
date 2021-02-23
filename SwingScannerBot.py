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
import psycopg2#IMPORT TO STREAMLIT
from configparser import ConfigParser
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


# In[7]:


def config(filename = 'database.ini', section = 'postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def connect():
    """ Connect to the PostgreSQL database server """
    st.write('connect was run')
    conn = None
    try:
        # read connection parameters
        #params = config()

        # connect to the PostgreSQL server
        st.write('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(database = "tickerbase", user = "postgres", host = "localhost", password = "wVfhac5c")

        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        st.write('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        st.write(db_version)
       
	# close the communication with the PostgreSQL
        
    except (Exception, psycopg2.DatabaseError) as error:
        st.write(error)

def fetchtickerdata():
    tickerdata = {}
    
    
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT ticker, alerted_price, entrytime FROM tickertracker ")
        rows = cur.fetchall()
        cur.close()
        for row in rows:
            newdict = {}
            newdict["alerted price"] = row[1]
            newdict["date of entry"] = str(row[2])
            ticker = yf.Ticker(row[0].replace(" ",""))
            newdict["current price"] = ticker.info['ask']
            tickerdata[row[0].replace(" ","")] = newdict
        return tickerdata
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    

    
def positionstable():
   
    tickerdict = fetchtickerdata()
    df = pd.DataFrame.from_dict(tickerdict)
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
connect()
st.table(positionstable())
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




