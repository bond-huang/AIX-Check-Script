#!/usr/bin/python3
#######################################################################
################## Check the AIX system filesystems! ##################
#######################################################################
import os
import re
import time
from functools import reduce
class FilesystemCheck():
    # Check the filesystem with usage rate over 80%
    def high_utili_fs(self):
        high_fs_cmd = 'df -k |awk \'NR>1{\
            if ($1 != "/proc" && ($3 / $2) < 0.2 ) print $7}\''
        high_fs = os.popen(high_fs_cmd)
        high_fs = high_fs.read()
        if len(high_fs) == 0:
            high_fs_result = 'No filesystem used over 80% was found.'
        else:
            high_fs = high_fs.strip()
            high_fs = high_fs.replace('\n',',')
            high_fs_result = 'Warning,filesystem used over 80%:'+ high_fs
        return high_fs_result
    # Check whether the filesystem of rootvg is mounted
    def unmount_fsck(self):
        rootvg_fs = ['/dev/hd4','/dev/hd2','/dev/hd9var',\
            '/dev/hd3','/dev/hd1','/dev/hd11admin','/proc',\
            '/dev/hd10opt','/dev/livedump']
        mount_fs_cmd = 'df -g'
        mount_fs = os.popen(mount_fs_cmd)
        mount_fs = mount_fs.read().strip()
        unmount_fslist = []
        for fs in rootvg_fs:
            if not re.findall(fs,mount_fs):
                unmount_fslist.append(fs)
        if len(unmount_fslist) == 0:
            unmount_result = "All filesystem of rootvg is mounted."
        else:
            unmount_fs = reduce(lambda x,y:x+','+y,unmount_fslist)
            unmount_result = 'Warning,unmount filesystem of rootvg:'+ unmount_fs
        return unmount_result
