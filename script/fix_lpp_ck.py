#!/usr/bin/python3
########################################################################
############## Check the AIX system fix filesets and lpp! ##############
########################################################################
import os
import re
class FixLppCheck():
    # Check the AIX system fix filesets
    def fix_check(self):
        fix_info_cmd = 'instfix -i | grep ML'
        fix_info = os.popen(fix_info_cmd)
        ostl_cmd = 'oslevel -s |awk -F- \'{print $2}\''
        ostl = os.popen(ostl_cmd)
        ostl = ostl.read().strip()
        item_num = int(ostl) + 2
        count = 0
        for i in fix_info:
            count += 1
            if not re.findall('were found.',i):
                fixck_result = 'Warning,some filesets for \
                    this system ware not found,please check!'
                break
        if item_num == count:
            fixck_result = 'All filesets for this OS level were found.'
        else:
            fixck_result = 'Warning,some filesets for \
                    this system ware not found,please check!'
        return fixck_result
    def lpp_check(self):
        lpp_ck_cmd = 'lppchk -v 2> /dev/null;echo $?'
        lpp_ck = os.popen(lpp_ck_cmd)
        lpp_ck = lpp_ck.read().strip()
        if len(lpp_ck) == 0:
            lppck_result = 'The lppchk command returns zero \
                and no errors were found.'
        else:
            lppck_result = 'Warning,the lppchk command found some \
                filesets need to be installed,please check!'
        return lppck_result
