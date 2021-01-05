#!/usr/bin/python3
######################################################################
#################### Check the AIX system rootvg! ####################
######################################################################
import os
import re
import time
class RootvgCheck():
    # Get rootvg state
    def vg_state(self):
        vg_state_cmd = 'lsvg rootvg |grep STATE |awk \'{print $3}\''
        vg_state = os.popen(vg_state_cmd)
        vg_state = vg_state.read().strip()
        vg_state_dict = {'item':'Rootvg State',\
            'value':vg_state,'remarks':'Must be active'}
        return vg_state_dict
    # Get rootvg disk member 
    def vg_disk(self):
        vg_disk_cmd = 'lsvg -p rootvg |awk \'NR>2{print $1}\''
        vg_disk = os.popen(vg_disk_cmd)
        vg_disk = vg_disk.read().strip()
        vg_disk = vg_disk.replace('\n','/')
        vg_disk_dict = {'item':'Rootvg Disk Member',\
            'value':vg_disk,'remarks':'N/A'}
        return vg_disk_dict
    # Get total PPs
    def total_pps(self):
        total_pps_cmd = 'lsvg rootvg |\
            sed -n \'/TOTAL PPs/p\'|awk \'{print $6}\''
        total_pps = os.popen(total_pps_cmd)
        total_pps = total_pps.read().strip()
        total_pps_dict = {'item':'Total PPs:',\
            'value':total_pps,'remarks':'N/A'}
        return total_pps_dict
    # Get free PPs
    def free_pps(self):
        free_pps_cmd = 'lsvg rootvg |\
            sed -n \'/FREE PPs/p\'|awk \'{print $6}\''
        free_pps = os.popen(free_pps_cmd)
        free_pps = free_pps.read().strip()
        free_pps_dict = {'item':'Free PPs:',\
            'value':free_pps,'remarks':'Pay attention if less'}
        return free_pps_dict
    # Get PP size
    def pp_size(self):
        pp_size_cmd = 'lsvg rootvg |\
            sed -n \'/PP SIZE/p\'|awk \'{print $6}\''
        pp_size = os.popen(pp_size_cmd)
        pp_size = pp_size.read().strip() + 'MB'
        pp_size_dict = {'item':'PP Size:',\
            'value':pp_size,'remarks':'N/A'}
        return pp_size_dict
    # Check the rootvg disk member whether is in the bootlist
    def bootlist_ck(self):
        disk_list_cmd = 'lsvg -p rootvg |awk \'NR>2{print $1}\''
        disk_list = os.popen(disk_list_cmd)
        bootlist_cmd = 'bootlist -m normal -o'
        bootlist = os.popen(bootlist_cmd)
        bootlist = bootlist.read().strip()
        bootck_result = 'Yes'
        for disk in disk_list:
            disk = disk.strip() + ' blv=hd5'
            if not re.findall(disk,bootlist):
                bootck_result = 'No'
                break
        bootlist_ck_dict = {'item':'Rootvg disks all on bootlist?',\
            'value':bootck_result,'remarks':'Please check and add if No'}
        return bootlist_ck_dict
    # Check the rootvg mirror
    def mirror_ck(self):
        unmirrorlv_cmd = 'lsvg -l rootvg | \
            awk \'NR>2{if ($1 != "lg_dumplv" && ($4 / $3) == 1)print $1}\''
        unmirror_lv = os.popen(unmirrorlv_cmd)
        unmirror_lv = unmirror_lv.read()
        if len(unmirror_lv) == 0:
            mirror_state = 'Yes'
            mirror_result = 'Rootvg mirror except lg_dumplv'
        else:
            mirror_state = 'No'
            unmirror_lv = unmirror_lv.strip()
            unmirror_lv = unmirror_lv.replace('\n','/')
            mirror_result = 'Unmirror LV:'+unmirror_lv
        bootlist_ck_dict = {'item':'Rootvg have a mirror?',\
            'value':mirror_state,'remarks':mirror_result}
        return bootlist_ck_dict
    # Check the rootvg LV is syncd or stale
    def syncd_ck(self):
        stale_lv_cmd = 'lsvg -l rootvg |grep stale | awk \'{print $1}\''
        stale_lv = os.popen(stale_lv_cmd)
        stale_lv = stale_lv.read().strip()
        if len(stale_lv) == 0:
            syncd_state = 'Yes'
            syncd_result = 'All must be syncd'
        else:
            syncd_state = 'No'
            stale_lv = stale_lv.replace('\n','/')
            syncd_result = 'Stale LV:'+stale_lv
        syncd_ck_dict = {'item':'All LVs are syncd?',\
            'value':syncd_state,'remarks':syncd_result}
        return syncd_ck_dict
    # Check the rootvg LV is open or close
    def open_ck(self):
        close_lv_cmd = 'lsvg -l rootvg |grep closed |\
            awk \'{if ($1 != "hd5")print $1}\''
        close_lv = os.popen(close_lv_cmd)
        close_lv = close_lv.read().strip()
        if len(close_lv) == 0:
            open_state = 'Yes'
            open_result = 'All LVs open except hd5'
        else:
            open_state = 'No'
            close_lv = close_lv.replace('\n','/')
            open_result = 'Close LV:'+close_lv
        open_ck_dict = {'item':'All LVs are open?',\
            'value':open_state,'remarks':open_result}
        return open_ck_dict
    # Check the primary dump LV
    def dump_primary(self):
        primary_lv_cmd = 'sysdumpdev -l|grep primary |awk \'{print $2}\''
        primary_lv = os.popen(primary_lv_cmd)
        primary_lv = primary_lv.read().strip()
        primary_lv_dict = {'item':'Primary dump LV',\
            'value':primary_lv,'remarks':'Please set if not lg_dumplv'}
        return primary_lv_dict
    # Get the dump status of "forced copy flag" 
    def force_cppy(self):
        force_copy_cmd = 'sysdumpdev -l |grep forced |awk \'{print $4}\''
        force_copy = os.popen(force_copy_cmd)
        force_copy = force_copy.read().strip()
        force_copy_dict = {'item':'Forced copy flag',\
            'value':force_copy,'remarks':'Please set if not true'}
        return force_copy_dict
    # Get the dump status of "always allow dump" 
    def always_dump(self):
        always_dump_cmd = 'sysdumpdev -l |grep always |awk \'{print $4}\''
        always_dump = os.popen(always_dump_cmd)
        always_dump = always_dump.read().strip()
        always_dump_dict = {'item':'Always allow dump',\
            'value':always_dump,'remarks':'Please set if not true'}
        return always_dump_dict
    # Get dump status of "Dump compression"
    def dump_comp(self):
        dump_comp_cmd = 'sysdumpdev -l |grep compression |awk \'{print $3}\''
        dump_comp = os.popen(dump_comp_cmd)
        dump_comp = dump_comp.read().strip()
        dump_comp_dict = {'item':'Dump compression',\
            'value':dump_comp,'remarks':'Please set if OFF'}
        return dump_comp_dict
    # Check the last backup time
    def backup_check(self):
        image_ck_cmd = 'ls -l /image.data 2> /dev/null'
        image_ck = os.popen(image_ck_cmd)
        image_ck = image_ck.read().strip()
        if len(image_ck) == 0:
            backup_time = "N/A"
            backup_result = 'Image.data cannot be found'
        else:
            backup_time_cmd = 'os.path.getmtime(\'/image.data\')'
            backup_time = os.popen(backup_time_cmd)
            backup_time = backup_time.read().strip()
            backup_time = time.gmtime(backup_time)
            backup_time = time.strftime('%Y/%m/%d',backup_time)
            backup_result = 'Pay attention If time is longer'
        back_time_dict = {'item':'Rootvg last backup time',\
            'value':backup_time,'remarks':backup_result}
        return back_time_dict
    # Sort data
    def rootvg_sort(self):
        rootvg_list = []
        rootvg_list.extend([self.vg_state(),self.vg_disk(),\
            self.total_pps(),self.free_pps(),self.pp_size(),\
            self.bootlist_ck(),self.mirror_ck(),self.syncd_ck(),\
            self.open_ck(),self.dump_primary(),self.force_cppy(),\
            self.always_dump(),self.dump_comp(),self.backup_check()])
        return rootvg_list
