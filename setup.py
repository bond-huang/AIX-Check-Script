#!/usr/bin/python3
####################################################################
################### Start check the AIX system! ####################
####################################################################
import os
import time
import jinja2
from script.sys_info import GetInfo
from script.err_check import ErrCheck
from script.perf_check import PerfCheck
from script.rootvg_ck import RootvgCheck
from script.fs_check import FilesystemCheck
from script.fix_lpp_ck import FixLppCheck
from script.device_check import DeviceCheck
from script.path_check import PathCheck
from script.sys_check import SystemCheck
# Check the user
user = os.popen('whoami')
user = user.read().strip()
if user != 'root':
    print('Please use the root user to run this script!')
    quit()
# Render funciton
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
time.sleep(1)
print('')

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
time.sleep(1)
print('')

# Check the system performance
print('Check the system performance,please waiting...')
perf_check = PerfCheck()
print('Check the system CPU performance,please waiting...')
cpuperf_list = perf_check.cpu_perf()
print('Check the system Memory performance,please waiting...')
mem_ps_list = perf_check.mem_perf()
mem_description = perf_check.mem_analyze()
print('Get the system disk performance data,please waiting...')
all_disk_iostat = perf_check.disk_perf()
print('Get the system adapter performance data,please waiting...')
all_adapter_iostat = perf_check.adapter_perf()
print('Check system performance is complete!')
time.sleep(1)
print('')

# Check the system rootvg
print('Check the system rootvg,please waiting...')
rootvg_check = RootvgCheck()
rootvg_list = rootvg_check.rootvg_sort()
print('Check system rootvg is complete!')
time.sleep(1)
print('')

# Check the filesystems
print('Check the filesystems,please waiting...')
filesystem_check = FilesystemCheck()
print('Check the filesystems usage rate,please waiting...')
high_fs_result = filesystem_check.high_utili_fs()
print('Check the unmount filesystems of rootvg,please waiting...')
unmount_result = filesystem_check.unmount_fsck()
print('Check filesystems is complete!')
time.sleep(1)
print('')

# Check the system fix and lpp filesets
print('Check the system fix and lpp filesets,please waiting...')
fix_lpp_check = FixLppCheck()
print('Check the AIX system fix filesets,please waiting...')
fixck_result = fix_lpp_check.fix_check()
print('Check the AIX system lpp filesets,please waiting...')
lppck_result = fix_lpp_check.lpp_check()
print('Check system fix filesets and lpp is complete!')
time.sleep(1)
print('')

# Check the system adapter information
print('Check the system adapter information,please waiting...')
device_check = DeviceCheck()
print('Get the system hdisk information,please waiting...')
all_hdisk_info = device_check.hdisk_info()
hdisk_note = device_check.hdisk_description()
print('Check the system adapter status,please waiting...')
adapter_abnormal_result = device_check.adapter_check()
print('Get the system vscsi and fscsi information,please waiting...')
all_scsi_fc_info = device_check.scsi_fc_info()
print('Check the system adapter information is complete!')
time.sleep(1)
print('')

# Check the system device path
print('Check the MPIO device path,please waiting...')
path_check = PathCheck()
print('Check the MPIO device abnormal path,please waiting...')
abnormal_path_result = path_check.result_sort()
print('Check the MPIO device path is complete!')
time.sleep(1)
print('')

# Check the system process and ulimit setting
print('Check the process and ulimit setting,please waiting...')
system_check = SystemCheck()
print('Get the last upgrade time of the AIX system,please waiting...')
upgrade_time_result = system_check.upgrade_time_format()
print('Get the last reboot time of the AIX system,please waiting...')
reboot_time_result = system_check.reboot_time_format()
print('Check whether the system has restarted after upgrade,please waiting...')
reboot_ck_result = system_check.determine()
print('Check the errdemon process,please waiting...')
errdemon_result = system_check.errdemon_check()
print('Check the srcmstr process,please waiting...')
srcmstr_result = system_check.srcmstr_check()
print('Get the system ulimit setting information,please waiting...')
ulimit_list = system_check.ulimit_check()
print('Check the system process and ulimit setting is complete!')
time.sleep(1)
print('')

# Generate html report
print('Generate HTML report,please waiting...')
content = render('base.html',**locals())
with open('report.html','w') as f:
    f.writelines(content)
    f.close()
print('Generate HTML report is complete!')



