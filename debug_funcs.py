cd
cd C:\Users\thoma\github\usd_cad_nn
import get_data as gd
import pandas as pd
import numpy as np
import quandl

# import data
USDCAD= quandl.get("FED/RXI_N_B_CA", authtoken="mmpvRYssGGBNky867tt5")

# US overnight rates
EffFedRate = quandl.get("FED/RIFSPFF_N_D", authtoken="mmpvRYssGGBNky867tt5", start_date='1980-01-01')
FedUppTarRange= quandl.get("FRED/DFEDTARU", authtoken="mmpvRYssGGBNky867tt5")
FedLowTarRange= quandl.get("FRED/DFEDTARL", authtoken="mmpvRYssGGBNky867tt5")
FedHisTarRate=quandl.get("FRED/DFEDTAR", authtoken="mmpvRYssGGBNky867tt5", start_date='1980-01-01')

#US yield curve rates since 1990
USyields = quandl.get("USTREASURY/YIELD", authtoken="mmpvRYssGGBNky867tt5")

#net cad long/short spec and non-speculative positions
NetCAD=quandl.get("CFTC/CD_F_L_ALL", authtoken="mmpvRYssGGBNky867tt5")

#oil prices futures weekly - Calculate backwardation/contango
Oil4 = quandl.get("EIA/PET_RCLC4_W", authtoken="mmpvRYssGGBNky867tt5")
Oil4.columns=['Oil4']
Oil1 = quandl.get("EIA/PET_RCLC1_W", authtoken="mmpvRYssGGBNky867tt5")
Oil1.columns=['Oil1']

#oil spot
Oilspot = quandl.get("FRED/DCOILWTICO", authtoken="mmpvRYssGGBNky867tt5")
Oilspot.columns=['Oilspot']
# Rig count
RigsUS = quandl.get("BKRHUGHES/COUNT_BY_TRAJECTORY", authtoken="mmpvRYssGGBNky867tt5")
RigsUS['RigsDelta']=RigsUS['Total']-RigsUS['Total'].shift()
RigsUS=RigsUS[['Total','RigsDelta']]

#US oil inventories
OilInv = quandl.get("EIA/WCESTUS1", authtoken="mmpvRYssGGBNky867tt5")
OilInv.columns=['Inv']
OilInv['InvDelta']=OilInv['Inv']-OilInv['Inv'].shift()


#USCPI
CPI = quandl.get("YALE/SP_CPI", authtoken="mmpvRYssGGBNky867tt5", start_date="1979-12-30")
CPI.columns=['CPI']

#Cad Bonds
CADBOC= pd.read_csv('CanBonds.csv',skiprows=4, index_col=['Rates'],skipfooter=7).convert_objects(convert_numeric=True)# CANSIM table 176-0043

#BoC overnight rates
BOCON= pd.read_csv('BoCOvernight.csv',skiprows=2, index_col=['Daily'])#CANSIM table 176-0048
BOCON.columns=['BOC fundrate']
BOCON.dropna(inplace=True)

# Employment numbers
USUnEm=quandl.get("FRED/UNRATE", authtoken="mmpvRYssGGBNky867tt5",start_date='1955-06-01')
USUnEm.columns=['Unemployment rate US']
USNonFarm=quandl.get("BLSE/CES0000000001", authtoken="mmpvRYssGGBNky867tt5",start_date='1955-06-01')
USNonFarm.columns=['1000s employed US']
employmentsituationdate=pd.DataFrame(pd.read_excel('EmploySitUS.xls',skiprows=35).iloc[:,0])
employmentsituationdate.columns=['date']
rest=pd.merge(USUnEm, employmentsituationdate,left_index=True, right_on='date',how='outer')
rest=rest.set_index('date')
rest.sort_index(level=0)
rest=pd.merge(rest, USNonFarm,left_index=True, right_index=True,how='outer')
rest['released']=rest['Unemployment rate US'].shift(2)
rest.fillna(method='pad',inplace=True)
# rest.tail(10)
emp=pd.merge(employmentsituationdate,rest,left_on='date',right_index=True)
emp.drop(['Unemployment rate US'],axis=1, inplace=True)
emp=emp.set_index('date')


CanEm=pd.read_csv('CanEmploy.csv',skiprows=3, index_col=['Data type']) #Cansim table 282-0087
CanEm=CanEm.iloc[0:3,5:].T['Seasonally adjusted']
CanEm.columns=[['1000s employed Can','Unemployment rate Can']]
CanEm1=CanEm.shift()
CanEm1.columns=[['C1000s employed shift1','CUnemploy rate shift1']]
CanEm2=CanEm.shift(2)
CanEm2.columns=[['C1000s employed shift2','CUnemploy rate shift2']]
CanEmS=pd.merge(CanEm1,CanEm2, left_index=True,right_index=True)
CanEmS['gainrateemp']=(CanEmS['C1000s employed shift1'].values-CanEmS['C1000s employed shift2'].values)/CanEmS['C1000s employed shift2']*100
CanEmS['gainrateunem']=CanEmS['CUnemploy rate shift1'].values-CanEmS['CUnemploy rate shift2'].values
CanEmS.index=pd.to_datetime(CanEmS.index)
CanEmSF=CanEmS[['CUnemploy rate shift1','CUnemploy rate shift2','gainrateemp','gainrateunem']]
# CanEmS.index.values=CanEmS.index.values.apply(lambda x: x.replace(day=1) )


daysahead=20
Currt= USDCAD
Currt['Plus1']=Currt['Value'].shift(periods=-daysahead) # THIS IS THE 20 DAY AHEAD PRICE
Currt['Minus1']=(Currt['Value'].shift(periods=1)-Currt['Value'])*100
# Utest['Minus5']=(Currt['Value'].shift(periods=5)-Currt['Value'])*100
Currt['Minus5']=(Currt['Value'].rolling(5).mean()-Currt['Value'])*100
Currt['Minus30']=(Currt['Value'].rolling(30).mean()-Currt['Value'])*100
Currt['Minus100']=(Currt['Value'].rolling(100).mean()-Currt['Value'])*100
Currt['Gain']=Currt['Plus1']-Currt['Value']
Currt['Result']=np.where(Currt['Gain']>0,1,0)
Currt=Currt[['Value','Minus1','Minus5','Minus30', 'Minus100','Result','Gain']]
Currt.columns=[['Current','Minus1','Minus5','Minus30', 'Minus100','Result','Gain']]
Curr=Currt.iloc[100:]

Oil=pd.merge(Oilspot, Oil1, how='outer', left_index=True, right_index=True,suffixes=('_spot','_C1'))
Oil=pd.merge(Oil, Oil4, how='outer', left_index=True, right_index=True)
Oil=pd.merge(Oil, OilInv, how='outer', left_index=True, right_index=True)
Oil=pd.merge(Oil, CPI, how='outer', left_index=True, right_index=True)
Oil=pd.merge(Oil, RigsUS, how='outer', left_index=True, right_index=True)
Oil.fillna(method='pad', inplace=True)
Oil['Gain_day']=Oil['Oilspot']-Oil['Oilspot'].shift()
Oil.dropna(inplace=True)
Oil['1MonthCurve']=Oil['Oilspot']-Oil['Oil1']
Oil['4MonthCurve']=Oil['Oilspot']-Oil['Oil4']
Oil['CPI']=Oil['CPI']/Oil['CPI'].iloc[0]
# CPI Corrections
Oil['SpotC']=Oil['Oilspot']/Oil["CPI"]
Oil['Oil4C']=Oil['Oil4']/Oil["CPI"]
Oil['Oil1C']=Oil['Oil1']/Oil["CPI"]
Oil['1MonthCurveC']=Oil['1MonthCurve']/Oil["CPI"]
Oil['4MonthCurveC']=Oil['4MonthCurve']/Oil["CPI"]
Oil['Gain_dayC']=Oil['Gain_day']/Oil["CPI"]
#Normalizing prices, inventory, rig count
OilC=Oil[['SpotC','Oil1C','Oil4C']]
OilD=Oil[['1MonthCurveC','4MonthCurveC','Gain_dayC','InvDelta','RigsDelta']]
OilD=(OilD-OilD.mean())/OilD.std()
OilC=OilC/OilC.mean(axis=0)
OilE=Oil[['Inv','Total']]
OilE=OilE/OilE.mean()

OilN=pd.merge(OilC, OilD, left_index=True, right_index=True)
OilN=pd.merge(OilN, OilE, left_index=True, right_index=True)
OilN.columns=[['SpotC', 'Oil1C', 'Oil4C', '1MonthCurveC', '4MonthCurveC', 'Gain_dayC',
	   'InvDelta', 'RigsDelta', 'Inv', 'RigsUS']]

Bonds=pd.merge(CADBOC,USyields,left_index=True,right_index=True, how='outer')
Bonds
Bonds.drop(['1 MO','3 MO','6 MO','20 YR'], axis=1,inplace=True)
Bonds.fillna(method='pad',inplace=True)
Bonds.dropna(inplace=True)
Bonds['2dif']=Bonds['Selected Government of Canada benchmark bond yields: 2 year']-Bonds['2 YR']
Bonds['5dif']=Bonds['Selected Government of Canada benchmark bond yields: 5 year']-Bonds['5 YR']
Bonds['10dif']=Bonds['Selected Government of Canada benchmark bond yields: 10 years']-Bonds['10 YR']

# Fed Funds target rate
fedfunds=pd.merge(FedUppTarRange,FedHisTarRate, how='outer', left_index=True,right_index=True)
fedfunds.fillna(method='pad',inplace=True,axis=1)
fedfunds.drop(['Value'], inplace=True,axis=1)
fedfunds.columns=['US fundrate']

BOCON['BOC fundrate'].replace(to_replace='..', method='ffill', inplace=True)
BOCON['BOC fundrate']=pd.to_numeric(BOCON['BOC fundrate'],downcast='float')
BOCON['BOC fundrate'].replace(to_replace=0.0, method='ffill', inplace=True)

FundsRates=pd.merge(BOCON,fedfunds,how='inner',left_index=True,right_index=True)
FundsRates['fundif']=FundsRates['BOC fundrate']-FundsRates['US fundrate']

#Speculative positions
NetCAD['NetSpec']=NetCAD['Noncommercial Long']-NetCAD['Noncommercial Short']
NetSp=NetCAD['NetSpec']
NetSp=(NetSp-NetSp.mean())/NetSp.std()

#Jobs
Jobs=pd.merge(emp,CanEmSF,left_index=True,right_index=True,how='outer')
Jobs=Jobs/(Jobs.max())*5 #Arbitrary 5 to achieve std of 1--- dividing by std did not work for some reason??

Bonds.head()

OilN.columns=OilN.columns.get_level_values(0)
OilN.columns
Jobs.columns
FundsRates.columns
Curr.columns=Curr.columns.get_level_values(0)
Curr.columns
CanEmS.columns.get_level_values(0)
emp.columns
CanEmSF.columns=CanEmSF.columns.get_level_values(0)
Currt.columns=Currt.columns.get_level_values(0)
Currt.columns
list(CanEmS.columns.levels)[0]
CanEmS.columns=CanEmS.columns.get_level_values(0)

    Curr.columns=Curr.columns.get_level_values(0)
    OilN.columns=OilN.columns.get_level_values(0)
    Feedt=pd.merge(Bonds,OilN,how='outer',left_index=True,right_index=True)
    Feedt=pd.merge(Feedt,FundsRates,how='outer',left_index=True,right_index=True)
    Feedt=pd.merge(Feedt,Jobs,how='outer',left_index=True,right_index=True)
    Feedt['NetSp']=NetSp
    Feedt.fillna(method='pad',inplace=True)
    Feedt=pd.merge(Curr,Feedt,how='outer',left_index=True,right_index=True)
    Feed=Feedt.copy()
    Feed.dropna(inplace=True) #this will drop all current prices too if the data has not been updated
    Y=Feed['Result']
    Ymag=Feed['Gain']
    Feed.drop(['Result','Gain'],axis=1, inplace=True)
    Feed=Feed.T
    Feedt.drop(['Result','Gain'],axis=1, inplace=True)
    Feedt.dropna(axis=0,inplace=True)
    Feedt=Feedt.T
    Y=Y.values.reshape(1,Feed.shape[1])
    Ymag=Ymag.values.reshape(1,Feed.shape[1])

Curr.columns
OilN.columns
Jobs.columns
Feedt.columns

import initit
import numpy as np
Y[:,Permuttrain]


X=Feed.values
percent_train=90
ntrain=int(percent_train/100*X.shape[1])
Permuttrain=list(np.random.permutation(ntrain))
Xtrain=np.float32(X[:,Permuttrain])
Ytrain=np.float32(Y[:,Permuttrain])
m=X.shape[1]
#     X=(X-X.mean(axis=1).reshape(-1,1))/X.std(axis=1).reshape(-1,1) ###### Batch normalization did not seem to have any effect
Permuttestdev= list(np.random.permutation(m-ntrain)+ntrain)
#     print(Permuttestdev)
ntest=len(Permuttestdev)//2
#     print(ntest)
Permuttest=Permuttestdev[:ntest]
Permutdev=Permuttestdev[ntest:]
Xtest=np.float32(X[:,Permuttest])
Ytest=np.float32(Y[:,Permuttest])
Xdev=np.float32(X[:,Permutdev])
Ydev=np.float32(Y[:,Permutdev])

Curr, Bonds, OilN, NetSp, FundsRates, Jobs=gd.get_data()
import datautils as du
Feed,Y,Ymag,FT=du.merge_all(Curr,Bonds,OilN,NetSp,FundsRates, Jobs)
du.SplitData3way(Feed.values,Y)

print('inputs are:',Feed.iloc[:,-5:])

git config --global user.email "thomasgmcarthur@gmail.com"
