#!/usr/bin/python3
#######################################################################
############### Check the AIX system Disk configuration ###############
#######################################################################
import os
import re
class DeviceCheck():
    def hdisk_info(self):
        hdisk_list_cmd = 'lspv |awk \'{print $1}\''
        hdisk_list = os.popen(hdisk_list_cmd)
        all_hdisk_info = []
        for hdisk in hdisk_list:
            hdisk = hdisk.strip()
            hdisk_status_cmd = 'lsdev -Cc disk |grep '\
                +hdisk+' |awk \'{print $2}\''
            hdisk_status = os.popen(hdisk_status_cmd)
            hdisk_status = hdisk_status.read().strip()
            hdisk_vg_cmd = 'lspv |awk \'{if ($1 == "'\
                +hdisk+'")print $3}\''
            hdisk_vg = os.popen(hdisk_vg_cmd)
            hdisk_vg = hdisk_vg.read().strip()
            hdisk_algorithm_cmd = 'lsattr -El '+hdisk+\
                ' |awk \'{if ($1 =="algorithm")print $2}\''
            hdisk_algorithm = os.popen(hdisk_algorithm_cmd)
            hdisk_algorithm = hdisk_algorithm.read().strip()
            hdisk_hcheck_cmd = 'lsattr -El '+hdisk+\
                ' |awk \'{if ($1 =="hcheck_interval")print $2}\''
            hdisk_hcheck = os.popen(hdisk_hcheck_cmd)
            hdisk_hcheck = hdisk_hcheck.read().strip()
            hdisk_hcmode_cmd = 'lsattr -El '+hdisk+\
                ' |awk \'{if ($1 =="hcheck_mode")print $2}\''
            hdisk_hcmode = os.popen(hdisk_hcmode_cmd)
            hdisk_hcmode = hdisk_hcmode.read().strip()
            hdisk_reserve_cmd = 'lsattr -El '+hdisk+\
                ' |awk \'{if ($1 =="reserve_policy")print $2}\''
            hdisk_reserve = os.popen(hdisk_reserve_cmd)
            hdisk_reserve = hdisk_reserve.read().strip()
            hdisk_pcm_cmd = 'lsattr -El '+hdisk+\
                ' |awk \'{if ($1 =="PCM")print $2}\''
            hdisk_pcm = os.popen(hdisk_pcm_cmd)
            hdisk_pcm = hdisk_pcm.read().strip()
            hdisk_info = {'hdisk':hdisk,'hdisk_status':hdisk_status,\
                'hdisk_vg':hdisk_vg,'hdisk_algorithm':hdisk_algorithm,\
                'hdisk_hcheck':hdisk_hcheck,'hdisk_hcmode':hdisk_hcmode,\
                'hdisk_reserve':hdisk_reserve,'hdisk_pcm':hdisk_pcm}
            all_hdisk_info.append(hdisk_info)
        return all_hdisk_info
    def hdisk_description(self):
        hdisk_note = '&#8195;&#8195;Please set the value according \
            to the official IBM recommendation.If the VG is shared, \
            such as the heartbeat VG and shared VG in PowerHA, \
            please set reserve_policy to no_reserve.'
        return hdisk_note
    def adapter_check(self):
        adapter_abnormal_cmd = 'lsdev -Cc adapter |\
            awk \'{if ($2 != "Available")print $1}\''
        adapter_abnormal = os.popen(adapter_abnormal_cmd)
        adapter_abnormal = adapter_abnormal.read().strip()
        if len(adapter_abnormal) == 0:
            adapter_abnormal_result = 'All adapter are Available!'
        else:
            adapter_abnormal = adapter_abnormal.replace('\n',',')
            adapter_abnormal_result = 'Fonud some abnormal adapter: '\
                +adapter_abnormal
        return adapter_abnormal_result
    def scsi_fc_info(self):
        vscsi_list_cmd = 'lsdev -Cc adapter|grep vscsi |\
            awk \'{if ($2 == "Available")print $1}\''
        vscsi_list = os.popen(vscsi_list_cmd)
        fscsi_list_cmd = 'lsdev -Cc adapter|grep fcs |\
            awk \'{if ($2 == "Available")print $1}\'|\
            sed \'s/fcs/fscsi/\''
        fscsi_list = os.popen(fscsi_list_cmd)
        all_scsi_fc_info = []
        for vscsi in vscsi_list:
            vscsi = vscsi.strip()
            vscsi_status_cmd = 'lsdev -Cc adapter |grep '\
                +vscsi+ '| awk \'{print $2}\''
            vscsi_status = os.popen(vscsi_status_cmd)
            vscsi_status = vscsi_status.read().strip()
            vscsi_err_recov_cmd = 'lsattr -El '+vscsi+\
                ' |grep err_recov|awk \'{print $2}\''
            vscsi_err_recov = os.popen(vscsi_err_recov_cmd)
            vscsi_err_recov = vscsi_err_recov.read().strip()
            vscsi_info = {'name':vscsi,'status':vscsi_status,\
                'vscsi_err_recov':vscsi_err_recov,'attach':'N/A',\
                'dyntrk':'N/A','fc_err_recov':'N/A'}
            all_scsi_fc_info.append(vscsi_info)
        for fscsi in fscsi_list:
            fscsi = fscsi.strip()
            fscsi_status_cmd = 'lsdev |grep '+fscsi+' |awk \'{print $2}\''
            fscsi_status = os.popen(fscsi_status_cmd)
            fscsi_status = fscsi_status.read().strip()
            fscsi_attach_cmd = 'lsattr -El '+fscsi+\
                ' |grep attach|awk \{print $2}\''
            fscsi_attach = os.popen(fscsi_attach_cmd)
            fscsi_attach = fscsi_attach.read().strip()
            fscsi_dyntrk_cmd = 'lsattr -El '+fscsi+\
                ' |grep dyntrk|awk \{print $2}\''
            fscsi_dyntrk = os.popen(fscsi_dyntrk_cmd)
            fscsi_dyntrk = fscsi_dyntrk.read().strip()
            fscsi_err_recov_cmd = 'lsattr -El '+fscsi+\
                ' |grep err_recov|awk \'{print $2}\''
            fscsi_err_recov = os.popen(fscsi_err_recov_cmd)
            fscsi_err_recov = fscsi_err_recov.read().strip()
            fscsi_info = {'name':fscsi,'status':fscsi_status,\
                'vscsi_err_recov':'N/A','attach':fscsi_attach,\
                'dyntrk':fscsi_dyntrk,'fc_err_recov':fscsi_err_recov}
            all_scsi_fc_info.append(fscsi_info)
        return all_scsi_fc_info
