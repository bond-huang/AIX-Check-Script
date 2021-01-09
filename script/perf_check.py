#!/usr/bin/python3
#############################################################################
##################### Check the AIX system performacne! #####################
#############################################################################
import os
import re
class PerfCheck():
    # Get and analyze CPU performance data.
    def cpu_perf(self):
        # Get the CPU Tpye
        type_cmd = 'lparstat -i |sed -n \'/Type/p\'|grep -i shared'
        cpu_type = os.popen(type_cmd)
        cpu_type = cpu_type.read()
        # Get performance data
        user_list = []
        sys_list = []
        use_list = []
        idle_list = []
        iowait_list = []
        entc_list = []
        iostat_cmd = 'iostat -t 1 5|awk \'{print $3,$4,$5,$6,$8}\'|tail -5'
        iostat = os.popen(iostat_cmd)
        # Sort the performance data
        for i in iostat:
            i = i.strip()
            i = i.split(' ')
            i = map(float,i)
            i = list(i)
            user_list.append(i[0])
            sys_list.append(i[1])
            idle_list.append(i[2])
            iowait_list.append(i[3])
            # Determine whether the CPU is shared or dedicated
            if len(cpu_type) != 0:
                entc_list.append(i[4])
        # Sort and analyze CPU usage
        for j in range(len(user_list)):
            usage_rate = round((user_list[j] + sys_list[j]),2)
            use_list.append(usage_rate)
        max_use = max(use_list)
        min_use = min(use_list)
        avg_use = round((sum(use_list) / len(use_list)),2)
        if avg_use > 90:
            use_state = 'Serious!CPU usage is high,handle it ASAP!'
        elif 70 < avg_use < 90:
            use_state = 'Warning!CPU usage is relatively high!'
        elif 50 < avg_use < 70:
            use_state = 'Attention!CPU usage needs attention!'
        else:
            use_state = 'Normal!The CPU usage is normal.'
        usage = {'name':'usage','max':max_use,\
            'min':min_use,'avg':avg_use,'state':use_state}
        # Sort and analyze CPU idle
        max_idle = max(idle_list)
        min_idle = min(idle_list)
        avg_idle = round((sum(idle_list) / len(idle_list)),2)
        if avg_idle < 10:
            idle_state = 'Serious!CPU idle is low,handle it ASAP!'
        elif 10 < avg_idle < 30:
            idle_state = 'Warning!CPU idle is relatively low!'
        elif 30 < avg_idle < 50:
            idle_state = 'Attention!CPU idle needs attention!'
        else:
            idle_state = 'Normal!The CPU idle is normal.'
        idle = {'name':'idle','max':max_idle,\
            'min':min_idle,'avg':avg_idle,'state':idle_state}
        # Sort and analyze CPU iowait
        max_iowait = max(iowait_list)
        min_iowait = min(iowait_list)
        avg_iowait = round((sum(iowait_list) / len(iowait_list)),2)
        iowait_state = 'It is a complex indicator,No analysis yet.'
        iowait = {'name':'iowait','max':max_iowait,\
            'min':min_iowait,'avg':avg_iowait,'state':iowait_state}
        # Organize CPU performance data
        cpuperf_list = []
        if len(cpu_type) == 0:
            cpuperf_list.extend([usage,idle,iowait])
        else:
            # Sort and analyze CPU entc
            max_entc = max(entc_list)
            min_entc = min(entc_list)
            avg_entc = round((sum(entc_list) / len(entc_list)),2)
            if avg_entc > 100:
                entc_state = 'Serious!More than Entitled Capacity,need add CPU!'
            else:
                entc_state = 'Less than Entitled Capacity,refer to the usage rate.'
            entc = {'name':'entc','max':max_entc,\
                'min':min_entc,'avg':avg_entc,'state':entc_state}
            cpuperf_list.extend([usage,idle,iowait,entc])
        return cpuperf_list
    # Get memory and page space performance data.
    def mem_perf(self):
        # Get Memory information
        mem_szcmd = 'prtconf -m | awk \'{print $3 $4}\''
        mem_size = os.popen(mem_szcmd)
        mem_size = mem_size.read().strip()
        mem_inusecmd = 'amepat |grep In-Use |awk \'{print $5}\''
        mem_inuse = os.popen(mem_inusecmd)
        mem_inuse = mem_inuse.read().strip() + 'MB'
        mem_usedcmd = 'amepat |grep In-Use |awk \'{print $7}\''
        mem_used = os.popen(mem_usedcmd)
        mem_used = mem_used.read().strip()
        mem_used = re.findall('.{3}',mem_used)[0]
        mem_active = 'N/A'
        mem_auto = 'N/A'
        # Get Page space information
        ps_szcmd = 'lsps -a |awk \'NR>1 {print $4}\''
        ps_size = os.popen(ps_szcmd)
        ps_size = ps_size.read().strip()
        ps_inusecmd = 'svmon -G | grep space |awk \'{print $4}\''
        ps_inuse = os.popen(ps_inusecmd)
        ps_inuse = int(ps_inuse.read().strip())
        ps_inuse = str(int(ps_inuse / 256 )) + 'MB'
        ps_usedcmd = 'lsps -a |awk \'NR>1 {print $5}\''
        ps_used = os.popen(ps_usedcmd)
        ps_used = ps_used.read().strip() + '%'
        ps_activecmd = 'lsps -a |awk \'NR>1 {print $6}\''
        ps_active = os.popen(ps_activecmd)
        ps_active = ps_active.read().strip()
        ps_autocmd = 'lsps -a |awk \'NR>1 {print $7}\''
        ps_auto = os.popen(ps_autocmd)
        ps_auto = ps_auto.read().strip()
        # Organize Memory and Page Space data
        mem_ps_list = []
        title = {'name':'Item','size':'Size',\
            'inuse':'Inuse','used':'Used',\
            'active':'Active','auto':'Auto'}
        memory = {'name':'Memory','size':mem_size,\
            'inuse':mem_inuse,'used':mem_used,\
            'active':mem_active,'auto':mem_auto}
        ps = {'name':'Page Space','size':ps_size,\
            'inuse':ps_inuse,'used':ps_used,\
            'active':ps_active,'auto':ps_auto}
        mem_ps_list.extend([title,memory,ps])
        return mem_ps_list
    # Analyze the memory and page space data
    def mem_analyze(self):
        mem_description = []
        note1 = 'Description:'
        note2 = '&#8195;&#8195;If the physical memory is almost exhausted \
            and the paging space usage is high,recommended \
            to increase physical memory.If the physical memory \
            is almost exhausted,but the paging space usage is very low,\
            and if the system is running a database,\
            check whether the database memory is sufficient,\
            if not,recommended to increase physical memory.'
        mem_description.extend([note1,note2])
        return mem_description
    # Check the system disk performance
    def disk_perf(self):
        disk_list_cmd = 'lspv |awk \'{print $1}\''
        disk_list = os.popen(disk_list_cmd)
        all_disk_iostat = []
        for disk in disk_list:
            disk = disk.strip()
            disk_iostat_cmd = 'iostat -d '+disk+' 1 5 |grep '\
                +disk+'| awk \'{print $2,$3,$4,$5,$6}\''
            disk_iostat = os.popen(disk_iostat_cmd)
            tm_act_list = []
            kbps_list = []
            tps_list = []
            Kb_read_list = []
            Kb_wrtn_list = []
            for i in disk_iostat:
                i = i.strip()
                i = i.split(' ')
                i = map(float,i)
                i = list(i)
                tm_act_list.append(i[0])
                kbps_list.append(i[1])
                tps_list.append(i[2])
                Kb_read_list.append(i[3])
                Kb_wrtn_list.append(i[4])
            max_tm_act = max(tm_act_list)
            avg_tm_act = round((sum(tm_act_list) / len(tm_act_list)),2)
            max_kbps = max(kbps_list)
            avg_kbps = round((sum(kbps_list) / len(kbps_list)),2)
            max_tps = max(tps_list)
            avg_tps = round((sum(tps_list) / len(tps_list)),2)
            max_Kb_read = max(Kb_read_list)
            avg_Kb_read = round((sum(Kb_read_list) / len(Kb_read_list)),2)
            max_Kb_wrtn = max(Kb_wrtn_list)
            avg_Kb_wrtn = round((sum(Kb_wrtn_list) / len(Kb_wrtn_list)),2)
            disk_pref_dict = {'disk':disk,'max_tm_act':max_tm_act,\
                'avg_tm_act':avg_tm_act,'max_kbps':max_kbps,\
                'avg_kbps':avg_kbps,'max_tps':max_tps,\
                'avg_tps':avg_tps,'max_Kb_read':max_Kb_read,\
                'avg_Kb_read':avg_Kb_read,'max_Kb_wrtn':max_Kb_wrtn,\
                'avg_Kb_wrtn':avg_Kb_wrtn}
            all_disk_iostat.append(disk_pref_dict)
        return all_disk_iostat
    # Check the system adapter performance
    def adapter_perf(self):
        adapter_list_cmd = 'iostat -a |awk \'{RS=""}\
            {if ($1 == "Vadapter:" || $1 == "Adapter:") \
            print $0}\'|sed \'/dapter:/d\'|awk \'{print $1}\''
        adapter_list = os.popen(adapter_list_cmd)
        all_adapter_iostat = []
        for adapter in adapter_list:
            adapter = adapter.strip()
            adapter_iostat_cmd = 'iostat -adt 1 5 |grep '\
                +adapter+' |awk \'{print $2,$3,$4,$5}\''
            adapter_iostat = os.popen(adapter_iostat_cmd)
            adp_kbps_list = []
            adp_tps_list = []
            bkread_list = []
            bkwrtn_list = []
            for i in adapter_iostat:
                i = i.strip()
                i = i.split(' ')
                i = map(float,i)
                i = list(i)
                adp_kbps_list.append(i[0])
                adp_tps_list.append(i[1])
                bkread_list.append(i[2])
                bkwrtn_list.append(i[3])
            max_adp_kbps = max(adp_kbps_list)
            avg_adp_kbps = round((sum(adp_kbps_list) / len(adp_kbps_list)),2)
            max_adp_tps = max(adp_tps_list)
            avg_adp_tps = round((sum(adp_tps_list) / len(adp_tps_list)),2)
            max_bkread = max(bkread_list)
            avg_bkread = round((sum(bkread_list) / len(bkread_list)),2)
            max_bkwrtn = max(bkwrtn_list)
            avg_bkwrtn = round((sum(bkwrtn_list) / len(bkwrtn_list)),2)
            adapter_pref_dict = {'adapter':adapter,\
                'max_adp_kbps':max_adp_kbps,'avg_adp_kbps':avg_adp_kbps,\
                'max_adp_tps':max_adp_tps,'avg_adp_tps':avg_adp_tps,\
                'max_bkread':max_bkread,'avg_bkread':avg_bkread,\
                'max_bkwrtn':max_bkwrtn,'avg_bkwrtn':avg_bkwrtn}
            all_adapter_iostat.append(adapter_pref_dict)
        return all_adapter_iostat
