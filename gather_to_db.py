import quandl
import pandas as pd
import numpy as np
import sqlite3
cd /Users/Thomas/github/usd_cad_NN/
import get_data
from datautils import *
from sqlalchemy import create_engine

Bonds, OilN, NetSp, FundsRates, Jobs=get_data.get_data()
Curr=get_data.get_curr()

Feed=merge_all_DB(Curr,Bonds, OilN, NetSp, FundsRates, Jobs)
Feed.index

conn = sqlite3.connect('currencydb.sqlite')
cur = conn.cursor()
engine=create_engine('sqlite:////Users/Thomas/github/usd_cad_NN/currencydb.sqlite')
connection=engine.raw_connection()
Feed.to_sql('currencydb', connection, if_exists='append')

# Curr.tail() #march3
# Bonds.tail(20)#march9
# OilN.tail()#march9
# NetSp.tail()#mar6
# FundsRates.tail()#Jan9
# Jobs.tail()#Feb2
