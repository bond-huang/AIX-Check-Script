#!/usr/bin/python3
#######################################################################
##################### Start check the AIX system! #####################
#######################################################################
import os
import jinja2
from script.sys_info import GetInfo
from script.err_check import ErrCheck
def render(tpl_path,**kwargs):
    path,falename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader('./')
    ).get_template('base.html').render(**kwargs)

# Get system information
print('System check in progress!')
print('Get system information,please waiting...')
get_info = GetInfo()
hostname = get_info.get_hostname()
items = get_info.info_arrange()
print('Get system information is complete!')

# Check the system error log for the past thirty days
print('Check the system error log for the past thirty days...')
err_check = ErrCheck()
# Check the system hardware error event
print('Check the Hardware errors event,please waiting...')
hwerr_result = err_check.hw_check()
# Check the system software error event
print('Check the Software errors event,please waiting...')
swerr_result = err_check.sw_check()
# Check the system errlogger information event
print('Check the Errlogger information event,please waiting...')
loggererr_result = err_check.logger_check()
# Check the system unknown error event
print('Check the Unknown error event,please waiting...')
unknownerr_result = err_check.unknown_check()
print('Check system error log is complete!')

# Generate html report
print('Generate HTML report,please waiting...')
content = render('base.html',**locals())
with open('report.html','w') as f:
    f.writelines(content)
    f.close()
print('Generate HTML report is complete!')
