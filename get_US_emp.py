
import urllib.request
import ssl
from bs4 import BeautifulSoup
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
#US nonfarm payroll and unemployment

def get_nonfarm_jobs():
    url=urllib.request.urlopen('https://www.bls.gov/news.release/empsit.t17.htm', context=ctx) #find the table from the web
    soup=BeautifulSoup(url, 'html.parser')
    right_table=soup.find('table', class_='regular')

    A=[]
    B=[]
    C=[]
    D=[]
    E=[]
    F=[]
    G=[]
    H=[]
    I=[]

    for row in right_table.findAll("tr"):
        cells = row.findAll('td')
        if len(cells)==9: #Only extract table body not heading
            A.append(cells[0].find(text=True))
            B.append(cells[1].find(text=True))
            C.append(cells[2].find(text=True))
            D.append(cells[3].find(text=True))
            E.append(cells[4].find(text=True))
            F.append(cells[5].find(text=True))
            G.append(cells[6].find(text=True))
            H.append(cells[7].find(text=True))
            I.append(cells[8].find(text=True))


    return int(I[0]), int(H[0].replace(',',''))
