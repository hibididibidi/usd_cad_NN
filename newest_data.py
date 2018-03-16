# cd /Users/Thomas/github/usd_cad_NN/
from get_US_emp import *
from currency_json import *
from get_Can_Bank import *
from get_US_Bank import *


XE=get_curr_xe() #Currency data
US_gain, US_total=get_nonfarm_jobs() #US Jobs data
Can_Bank=get_Can_bankrate() #BoC bank rate
US_Bank=get_US_bankrate() #Fed funds rate

# Can_Bank
# US_gain
# XE
#US_Bank
