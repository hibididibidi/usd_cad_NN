import urllib.request
import ssl
from bs4 import BeautifulSoup
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_Can_bankrate():
    url=urllib.request.urlopen('https://www.bankofcanada.ca/core-functions/monetary-policy/key-interest-rate/',context=ctx)
    soup=BeautifulSoup(url,'html.parser')
    right_table=soup.find('table', class_='table table-striped table-bordered table-hover')

    A=[]
    B=[]
    C=[]
    for line in right_table.findAll('tr'):
        row=line.findAll('td')
        if len(line.findAll('td'))==3:
            A.append(row[0].find(text=True))
            B.append(float(row[1].find(text=True)))
            C.append(row[2].find(text=True))
    return B[0]
# X=zip(A,B,C)
# X
# list(X)
