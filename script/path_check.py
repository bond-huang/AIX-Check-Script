#!/usr/bin/python3
#######################################################################
################### Check the AIX system disk path! ###################
#######################################################################
import os
class PathCheck():
    def disable_check(self):
        disable_cmd= 'lspath -F "name status path_id parent connection"\
            |grep -i disable'
        disable_path = os.popen(disable_cmd)
        disable_path = disable_path.read()
        disable_path_list = []
        if len(disable_path) == 0:
            disable_result = 'No disable path was found.'
        else:
            disable_path = os.popen(disable_cmd)
            for path in disable_path:
                path = path.strip()
                path = path.split(' ')
                name = path[0]
                status = path[1]
                path_id = path[2]
                parent = path[3]
                connection = path[4]
                disablepath = {'name':name,'status':status,\
                    'path_id':path_id,'parent':parent,\
                    'connection':connection}
                disable_path_list.append(disablepath)
            disable_result = disable_path_list
        return disable_result
    def defined_check(self):
        defined_cmd= 'lspath -F "name status path_id parent connection"\
            |grep -i defined'
        defined_path = os.popen(defined_cmd)
        defined_path = defined_path.read()
        defined_path_list = []
        if len(defined_path) == 0:
            defined_result = 'No defined path was found.'
        else:
            defined_path = os.popen(defined_cmd)
            for path in defined_path:
                path = path.strip()
                path = path.split(' ')
                name = path[0]
                status = path[1]
                path_id = path[2]
                parent = path[3]
                connection = path[4]
                definedpath = {'name':name,'status':status,\
                    'path_id':path_id,'parent':parent,\
                    'connection':connection}
                defined_path_list.append(definedpath)
            defined_result = defined_path_list
        return defined_result
    def missing_check(self):
        missing_cmd= 'lspath -F "name status path_id parent connection"\
            |grep -i missing'
        missing_path = os.popen(missing_cmd)
        missing_path = missing_path.read()
        missing_path_list = []
        if len(missing_path) == 0:
            missing_result = 'No missing path was found.'
        else:
            missing_path = os.popen(missing_cmd)
            for path in missing_path:
                path = path.strip()
                path = path.split(' ')
                name = path[0]
                status = path[1]
                path_id = path[2]
                parent = path[3]
                connection = path[4]
                missingpath = {'name':name,'status':status,\
                    'path_id':path_id,'parent':parent,\
                    'connection':connection}
                missing_path_list.append(missingpath)
            missing_result = missing_path_list
        return missing_result
    def failed_check(self):
        failed_cmd= 'lspath -F "name status path_id parent connection"\
            |grep -i failed'
        failed_path = os.popen(failed_cmd)
        failed_path = failed_path.read()
        failed_path_list = []
        if len(failed_path) == 0:
            failed_result = 'No failed path was found.'
        else:
            failed_path = os.popen(failed_cmd)
            for path in failed_path:
                path = path.strip()
                path = path.split(' ')
                name = path[0]
                status = path[1]
                path_id = path[2]
                parent = path[3]
                connection = path[4]
                failedpath = {'name':name,'status':status,\
                    'path_id':path_id,'parent':parent,\
                    'connection':connection}
                failed_path_list.append(failedpath)
            failed_result = failed_path_list
        return failed_result
    def result_sort(self):
        abnormal_path_result = []
        disable_info = self.disable_check()
        disable_dict = {'name':'disable','result':disable_info}
        defined_info = self.defined_check()
        defined_dict = {'name':'defined','result':defined_info}
        missing_info = self.missing_check()
        missing_dict = {'name':'missing','result':missing_info}
        failed_info = self.failed_check()
        failed_dict = {'name':'failed','result':failed_info}
        abnormal_path_result.extend([disable_dict,defined_dict,\
            missing_dict,failed_dict])
        return abnormal_path_result
