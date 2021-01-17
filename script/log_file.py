#!/usr/bin/python3
#######################################################################
##################### Archive system information! #####################
#######################################################################
import os
import time
class ArchiveInfo():
    # Save some command output.
    def cmd_log(self):
        pwd = os.getcwd()
        os.mkdir('log')
        os.popen('prtconf > log/prtconf.log;\
            lscfg -vp > log/lscfg.log;\
            lparstat -i > log/lparstat.log')
        time.sleep(3)
        os.popen('errpt -a > log/errpt.log')
        time.sleep(2)
        os.popen('df -g > log/df.log;\
            lsfs > log/lsfs.log;\
            lspv > log/lspv.log;\
            lsps -a > log/lsps.log;\
            lsdev > log/lsdev.log\
            lspath > log/lspath.log\
            lsvg -p rootvg > log/rootvg.log\
            lsvg -o | lsvg -il >> log/lsvg.log')
        os.popen('alog -ot boot > log/alog.log')
        time.sleep(2)
        os.popen('cat /etc/hosts > log/hosts.log;\
            cat /etc/filesystems > log/filesystems.log;\
            cat /etc/inittab > log/inittab.log;')
        time.sleep(3)
        os.popen('netstat -rn > log/netstat.log;\
            netstat -in >> log/netstat.log;\
            netstat -a >> log/netstat.log')
        time.sleep(2)
        os.popen('lsattr -El sys0 > log/sysattr.log')
        os.popen('lsdev -Cc disk |\
            awk \'{print "lsattr -El "$1""}\'|\
            sh > log/diskstat.log')
        os.popen('lspath |awk \'{print $3}\'|uniq|\
            awk \'{print "lsattr -El "$1""}\'|\
            sh > log/adapterstat.log')
        # Get the date and rename the directory
        time.sleep(2)
        today_date = time.time()
        today_date = time.gmtime(today_date)
        today_date = time.strftime('%y%m%d',today_date)
        os.rename('log','log_'+today_date)
