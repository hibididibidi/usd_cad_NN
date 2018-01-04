import numpy as np
import pandas as pd
import quandl
import tensorflow as tf
import requests
%matplotlib inline

Curr, Bonds, OilN, NetSp, FundsRates, Jobs=get_data()
merge_all()
