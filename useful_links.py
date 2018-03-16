
import urllib.request
import
from bs4 import BeautifulSoup
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
#US nonfarm payroll and unemployment
url=urllib.request.urlopen('https://www.bls.gov/news.release/empsit.nr0.htm', context=ctx).read()
soup=BeautifulSoup(url, 'html.parser')
soup.decode()
