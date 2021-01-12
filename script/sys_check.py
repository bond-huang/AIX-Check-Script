#!/usr/bin/python3
########################################################################
########### Check the AIX system process and ulimit setting! ###########
########################################################################
import os
import re
import time
class SystemCheck():
    # Get the last upgrade time of the AIX system
    def get_upgrade_time(self):
        upgrade_time_cmd = 'lslpp -h bos.rte|\
            awk \'{print \"\"$4,$5\"\"}\'|tail -1'
        upgrade_time = os.popen(upgrade_time_cmd)
        upgrade_time = upgrade_time.read(17)
        upgrade_time = time.strptime(upgrade_time,'%m/%d/%y %H:%M:%S')
        upgrade_time = time.mktime(upgrade_time)
        return upgrade_time
    # Format the upgrade time
    def upgrade_time_format(self):
        upgrade_ctime = self.get_upgrade_time()
        upgrade_ctime = time.ctime(upgrade_ctime)
        upgrade_time_result = 'The latest upgrade time is:'+ upgrade_ctime
        return upgrade_time_result
    # Get Get the last reboot time of the AIX system
    def get_reboot_time(self):
        reboot_time_cmd = 'alog -t boot -o|grep date|\
            awk \'{print \"\"$7,$8,$9,$10,$11,$12\"\"}\'|tail -1'
        reboot_time = os.popen(reboot_time_cmd)
        reboot_time = reboot_time.read(28)
        reboot_time = reboot_time.strip()
        reboot_time = time.strptime(reboot_time,'%a %b %d %H:%M:%S %Z %Y')
        reboot_time = time.mktime(reboot_time)
        reboot_time = reboot_time + 28800
        return reboot_time
    # Format the reboot time
    def reboot_time_format(self):
        reboot_ctime = self.get_reboot_time()
        reboot_ctime = time.ctime(reboot_ctime)
        reboot_time_result = 'The latest reboot time is:'+ reboot_ctime
        return reboot_time_result
    # Determine whether the system has reboot after the upgrade
    def determine(self):
        upgrade_time = self.get_upgrade_time()
        reboot_time = self.get_reboot_time()
        if upgrade_time < reboot_time:
            reboot_ck_result = 'The system has been restart after upgrade!'
        else:
            reboot_ck_result = 'The system did not restart after upgrade!'
        return reboot_ck_result
    # Check the errdemon process
    def errdemon_check(self):
        errdemon_cmd = 'ps -ef | grep errdemon|\
            sed -n \'/\/usr\/lib\/errdemon/p\''
        errdemon = os.popen(errdemon_cmd)
        errdemon = errdemon.read().strip()
        if len(errdemon) == 0:
            errdemon_result = 'The errdemon process is not running,\
                please start the process.'
        else:
            errdemon_result = 'The errdemon process is running.'
        return errdemon_result
    # Check the srcmstr process
    def srcmstr_check(self):
        srcmstr_cmd = 'ps -ef | grep srcmstr|\
            sed -n \'/\/usr\/sbin\/srcmstr/p\''
        srcmstr = os.popen(srcmstr_cmd)
        srcmstr = srcmstr.read().strip()
        if len(srcmstr) == 0:
            srcmstr_result = 'The srcmstr process is not running,\
                please start the process.'
        else:
            srcmstr_result = 'The srcmstr process is running.'
        return srcmstr_result
    # Get the system ulimit setting
    def ulimit_check(self):
        ulimit_list = []
        time_vaule = os.popen('ulimit -t')
        time_vaule = time_vaule.read().strip()
        time_dict = {'name':'time','unit':'seconds',\
            'vaule':time_vaule,'description':\
            'Specifies the No. of seconds to be used by each process'}
        file_vaule = os.popen('ulimit -f')
        file_vaule = file_vaule.read().strip()
        file_dict = {'name':'file','unit':'blocks',\
            'vaule':file_vaule,'description':'Sets the file size \
            limit in blocks when Limit parameter is used'}
        data_vaule = os.popen('ulimit -d')
        data_vaule = data_vaule.read().strip()
        data_dict = {'name':'data','unit':'K bytes',\
            'vaule':data_vaule,'description':\
            'Specifies the size of the data area'}
        stack_vaule = os.popen('ulimit -s')
        stack_vaule = stack_vaule.read().strip()
        stack_dict = {'name':'stack','unit':'K bytes',\
            'vaule':stack_vaule,'description':\
            'Specifies the stack size'}
        memory_vaule = os.popen('ulimit -m')
        memory_vaule = memory_vaule.read().strip()
        memory_dict = {'name':'memory','unit':'K bytes',\
            'vaule':memory_vaule,'description':\
            'Specifies the size of physical memory'}
        coredump_vaule = os.popen('ulimit -c')
        coredump_vaule = coredump_vaule.read().strip()
        coredump_dict = {'name':'coredump','unit':'512b blocks',\
            'vaule':coredump_vaule,'description':\
            'Specifies the size of core dumps'}
        nofiles_vaule = os.popen('ulimit -n')
        nofiles_vaule = nofiles_vaule.read().strip()
        nofiles_dict = {'name':'nofiles','unit':'descriptors',\
            'vaule':nofiles_vaule,'description':'Specifies limit \
            on the No. of file descriptors a process may have'}
        threads_vaule = os.popen('ulimit -r')
        threads_vaule = threads_vaule.read().strip()
        threads_dict = {'name':'threads','unit':'per process',\
            'vaule':threads_vaule,'description':'Specifies the \
            limit on the No. of threads a process can have'}
        processes_vaule = os.popen('ulimit -u')
        processes_vaule = processes_vaule.read().strip()
        processes_dict = {'name':'processes','unit':'per user',\
            'vaule':processes_vaule,'description':'Specifies the \
            limit on the No. of a process a user can create'}
        ulimit_list.extend([time_dict,file_dict,data_dict,\
            stack_dict,memory_dict,coredump_dict,nofiles_dict,\
            threads_dict,processes_dict])
        return ulimit_list
