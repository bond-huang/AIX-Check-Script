#!/usr/bin/python3
#############################################################################
################# Check the error log about the AIX system! #################
#############################################################################
import os
import re
import datetime
class ErrCheck():
    # Get the time thirty days ago
    def __get_time(self):
        nowtime = datetime.datetime.now()
        pasttime = nowtime + datetime.timedelta(days=-30)
        pastthirty = pasttime.strftime("%m%d%I%M%y")
        return pastthirty
    # Check the hardware error event in the AIX
    def hw_check(self):
        hw_ckcmd = 'errpt -dH -s '+ self.__get_time()
        hw_err = os.popen(hw_ckcmd)
        hw_err = hw_err.read()
        if len(hw_err) == 0:
            hwerr_result = 'No hardware error found in the system!'
        else:
            # Remove duplicate rows based on the IDENTIFIER column
            hw_err = os.popen(hw_ckcmd)
            hwerr_list = []
            for i in hw_err:
                j = i[0:10]
                k = [x[0:10] for x in hwerr_list]
                if not re.findall(j,str(k)):
                    hwerr_list.append(i)
            hw_err = ''.join(hwerr_list)
            hw_err = hw_err.strip()
            hwerr_result = 'Found some hardware event,please check:\n'+ hw_err
        return hwerr_result
    # Check the software error event in the AIX
    def sw_check(self):
        sw_ckcmd = 'errpt -dS -s '+ self.__get_time()
        sw_err = os.popen(sw_ckcmd)
        sw_err = sw_err.read()
        if len(sw_err) == 0:
            swerr_result = 'No software error found in the system!'
        else:
            # Remove duplicate rows based on the IDENTIFIER column
            sw_err = os.popen(sw_ckcmd)
            swerr_list = []
            for i in sw_err:
                j = i[0:10]
                k = [x[0:10] for x in swerr_list]
                if not re.findall(j,str(k)):
                    swerr_list.append(i)
            sw_err = ''.join(swerr_list)
            sw_err = sw_err.strip()
            swerr_result = 'Found some software event,please check:\n'+ sw_err
        return swerr_result
    # Check the errlogger information event in the AIX
    def logger_check(self):
        logger_ckcmd = 'errpt -dO -s '+ self.__get_time()
        logger_err = os.popen(logger_ckcmd)
        logger_err = logger_err.read()
        if len(logger_err) == 0:
            loggererr_result = 'No errlogger information event found in the system!'
        else:
            # Remove duplicate rows based on the IDENTIFIER column
            logger_err = os.popen(logger_ckcmd)
            loggererr_list = []
            for i in logger_err:
                j = i[0:10]
                k = [x[0:10] for x in loggererr_list]
                if not re.findall(j,str(k)):
                    loggererr_list.append(i)
            logger_err = ''.join(loggererr_list)
            logger_err = logger_err.strip()
            loggererr_result = 'Found some errlogger information event,please check:\n'+ logger_err
        return loggererr_result
    # Check the unknown error event in the AIX
    def unknown_check(self):
        unknown_ckcmd = 'errpt -dU -s '+ self.__get_time()
        unknown_err = os.popen(unknown_ckcmd)
        unknown_err = unknown_err.read()
        if len(unknown_err) == 0:
            unknownerr_result = 'No unknown event found in the system!'
        else:
            # Remove duplicate rows based on the IDENTIFIER column
            unknown_err = os.popen(unknown_ckcmd)
            unknownerr_list = []
            for i in unknown_err:
                j = i[0:10]
                k = [x[0:10] for x in unknownerr_list]
                if not re.findall(j,str(k)):
                    unknownerr_list.append(i)
            unknown_err = ''.join(unknownerr_list)
            unknown_err = unknown_err.strip()
            unknownerr_result = 'Found some unknown event,please check:\n'+ unknown_err
        return unknownerr_result
