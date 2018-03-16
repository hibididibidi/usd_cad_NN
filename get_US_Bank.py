import urllib.request
import ssl
from bs4 import BeautifulSoup
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_US_bankrate():
    url=urllib.request.urlopen('https://www.bankrate.com/rates/interest-rates/federal-funds-rate.aspx',context=ctx)
    soup=BeautifulSoup(url,'html.parser')
    right_table=soup.find('table')

    A=[]
    B=[]
    C=[]
    D=[]
    for line in right_table.findAll('tr'):
        row=line.findAll('td')
        if len(line.findAll('td'))==4:
            A.append(row[0].find(text=True))
            B.append(row[1].find(text=True))
            C.append(row[2].find(text=True))
            D.append(row[3].find(text=True))

    return float(B[1])
    # return B[0]
# X=zip(A,B,C)
# X
# list(X)
# A
# B
# C
# D
# class="tabledataoddnew"
# get_US_bankrate()
