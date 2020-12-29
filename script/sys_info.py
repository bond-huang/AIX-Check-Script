#!/usr/bin/python3
##################################################################################
############### Collect basic information about the AIX system! ##################
##################################################################################
import os
class GetInfo():
    # Get Power system Model and Type
    def get_type(self):
        cmd_type = 'uname -M |awk -F, \'{print $2}\''
        mtype = os.popen(cmd_type)
        mtype = mtype.read()
        return mtype.strip()
    # Get Power system Serial Number
    def get_sn(self):
        cmd_sn = 'prtconf |sed -n \'/Machine Serial Number/p\'|awk \'{print $4}\''
        sn = os.popen(cmd_sn)
        sn = sn.read()
        return sn.strip()
    # Get Power system Firmware level
    def get_fw(self):
        cmd_fw = 'prtconf | grep \"Platform Firmware level\"|awk \'{print $4}\''
        fw = os.popen(cmd_fw)
        fw = fw.read()
        return fw.strip()
    # Get AIX system date
    def get_time(self):
        pmdate = os.popen('date +%Y/%m/%d')
        pmdate = pmdate.read()
        return pmdate.strip()
    # Get AIX system host name
    def get_hostname(self):
        hostname = os.popen('hostname')
        hostname = hostname.read()
        return hostname.strip()
    # Get AIX system level
    def get_oslevel(self):
        oslevel = os.popen('oslevel -s')
        oslevel = oslevel.read()
        return oslevel.strip()
    # Get AIX system CPU configuration
    def get_cpu(self):
        cmd_cpu = 'lparstat -i |awk \'/Entitled Capacity[[:blank:]]{2}/{print $4}\''
        cpu = os.popen(cmd_cpu)
        cpu = cpu.read()
        return cpu.strip()
    # Get AIX system physical memory configuration
    def get_mem(self):
        cmd_mem = 'prtconf -m | awk \'{print $3 $4}\''
        memory = os.popen(cmd_mem)
        memory = memory.read()
        return memory.strip()
    # Get AIX system page space configuration
    def get_ps(self):
        cmd_ps = 'lsps -a | awk \'{if ($1 == \"hd6\") print $4}\''
        ps = os.popen(cmd_ps)
        ps = ps.read()
        return ps.strip()
    # Get AIX system IP configuration
    def get_ip(self):
        cmd_ip = 'prtconf |sed -n \'/IP Address:/p\'|awk \'{print $3}\''
        ip = os.popen(cmd_ip)
        ip = ip.read()
        return ip.strip()
    # Organize the data into a dictionary and add it to the list
    def info_arrange(self):
        item_list = []
        mtype = {'title':'Machine Typy','value':self.get_type()}
        sn = {'title':'Serial Number','value':self.get_sn()}
        fw = {'title':'Platform Firmware Level','value':self.get_fw()}
        pmdate = {'title':'Check Date','value':self.get_time()}
        hostname = {'title':'Host Name','value':self.get_hostname()}
        oslevel = {'title':'AIX Level','value':self.get_oslevel()}
        cpu = {'title':'CPU Entitled Capacity','value':self.get_cpu()}
        memory = {'title':'Memory Size','value':self.get_mem()}
        ps = {'title':'Page Space Size','value':self.get_ps()}
        ip = {'title':'IP Address','value':self.get_ip()}
        item_list.extend([mtype,sn,fw,pmdate,hostname,oslevel,cpu,memory,ps,ip])
        return item_list
