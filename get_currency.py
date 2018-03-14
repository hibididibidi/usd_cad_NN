import urllib
import ssl
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

html=urlopen('https://www.oanda.com/fx-for-business/historical-rates?utm_source=average_rates', context=ctx).read()
print(html)

for line in html:
