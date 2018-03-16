import urllib.request, urllib.parse, urllib.error
import json
import datetime
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_curr_xe():
    serviceurl = 'https://www.bankofcanada.ca/valet/observations/group/FX_RATES_DAILY/json?start_date=2017-03-09'
    # now=str(datetime.date.today())
    # now

    url = serviceurl
    uh = urllib.request.urlopen(url,context=ctx)
    data = uh.read().decode()
    js=json.loads(data)
    XE=js['observations'][-1]['FXUSDCAD']['v']
    return XE
