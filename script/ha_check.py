#!/usr/bin/python3
######################################################################
######################### Check the PowerHA! #########################
######################################################################
import os
import re
from functools import reduce
class HacmpCheck():
    cmd_path = '/usr/es/sbin/cluster/utilities/'
    # Check whether the system have HA cluster configuration
    def cluster_check(self):
        cltopinfo_cmd = self.cmd_path + 'cltopinfo 2> /dev/null'
        cltopinfo = os.popen(cltopinfo_cmd)
        cltopinfo = cltopinfo.read().strip()
        if len(cltopinfo) == 0:
            return False
        else:
            return True
    # Check whether the cluster service is started
    def ha_status(self):
        cldump_cmd = self.cmd_path + 'cldump 2> /dev/null'
        service_status = os.popen(cldump_cmd)
        service_status = service_status.read().strip()
        if len(service_status) == 0:
            return False
        else:
            return True
    # Get the cluster configuration information
    def cluster_cfginfo(self):
        cls_cfginfo_list = []
        cfginfo_cmd = self.cmd_path + 'cltopinfo'
        cfginfo = os.popen(cfginfo_cmd)
        cfginfo = cfginfo.read()
        # Get the HA Version
        HA_version_cmd = 'lslpp -l |grep cluster.es.server.rte \
            | tail -1 |awk \'{print $2}\''
        HA_version = os.popen(HA_version_cmd)
        HA_version = HA_version.read().strip()
        HA_version_dict = {'name':HA Version,'value':HA_version}
        # Get the Cluster Name
        cls_name = re.findall('Cluster Name:(.*)\n',cfginfo)
        cls_name = cls_name[0].strip()
        cls_name_dict = {'name':Cluster Name,'value':cls_name}
        # Get the Cluster Type
        cls_type = re.findall('Cluster Type:(.*)\n',cfginfo)
        cls_type = cls_type[0].strip()
        cls_type_dict = {'name':Cluster Type,'value':cls_tpye}
        # Get the Heartbat Type
        hb_tpye = re.findall('Heartbat Type:(.*)\n',cfginfo)
        hb_type = hb_tpye[0].strip()
        hb_tpye_dict = {'name':Heartbat Type,'value':hb_type}
        # Get the Repository Disk
        rep_disk = re.findall('Repository Disk:(.*)\n',cfginfo)
        rep_disk = rep_disk[0].strip()
        rep_disk_dict = {'name':Repository Disk,'value':rep_disk}
        # Get the Resource Group
        resource_grp_cmd = self.cmd_path + 'clmgr list node'
        resource_grp = os.popen(resource_grp_cmd)
        resource_grp = resource_grp.read().strip()
        resource_grp = resource_grp.replace('\n',',')
        resource_grp_dict = {'name':Resource Group,'value':resource_grp}
        # Sort the data
        cls_cfginfo_list.extend([HA_version_dict,cls_name_dict,\
            cls_type_dict,hb_tpye_dict,rep_disk_dict,resource_grp_dict])
        return cls_cfginfo_list
    # Get the cluster IP_label configuration information
    def cluster_ipinfo(self):
        ipinfo_cmd = self.cmd_path + 'cltopinfo -i |\
            sed -n \'/ether/p\''
        ipinfo = os.popen(ipinfo_cmd)
        ipinfo_list = []
        for iplabel in ipinfo:
            iplabel = iplabel.strip()
            iplabel = iplabel.split(' ')
            label_name = iplabel[0]
            label_network = iplabel[1]
            label_type = iplabel[2]
            label_node = iplabel[3]
            label_address = iplabel[4]
            lable_dict = {'name':label_name,'network':label_network,\
                'type':label_type,'node':label_node,\
                'address':label_address}
            ipinfo_list.append(lable_dict)
        return ipinfo_list
    # Get the cluster operating status
    def cls_status(self):
        cls_status_lsit = []
        # Get the cluster state
        cldump_info_cmd = self.cmd_path + 'cldump'
        cldump_info = os.popen(cldump_info_cmd)
        cldump_info = cldump_info.read()
        # Get the Cluster Name
        cluster_name = re.findall('Cluster Name:(.*)\n',cldump_info)
        cluster_name = cluster_name[0].strip()
        cluster_name_dict = {'name':Cluster Name,'state':cluster_name}
        # Get the Cluster State
        cluster_state = re.findall('Cluster State:(.*)\n',cldump_info)
        cluster_state = cluster_state[0].strip()
        cls_state_dict = {'name':Cluster State,'state':cls_tpye}
        # Get the Cluster Substate
        cluster_substate = re.findall('Cluster Substate:(.*)\n',cldump_info)
        cluster_substate = cluster_substate[0].strip()
        cls_substate_dict = {'name':Cluster Substate,'state':cluster_substate}
        # Get the cluster service subsystem state
        clshowsrv_cmd =  self.cmd_path + 'clshowsrv -v'
        clshowsrv = os.popen(clshowsrv_cmd)
        clshowsrv = clshowsrv.read()
        # Get the Cthags Subsystem state
        cthags_sub = re.findall('Cthags(.*)\n',clshowsrv)
        cthags_sub = cthags_sub[0].strip()
        cthags_state = re.findall('[a-z]*$',cthags_sub)
        cthags_state = cthags_state[0]
        cthags_dict = {'name':Cthags Subsystem,'state':cthags_state}
        # Get the Ctrmc Subsystem state
        ctrmc_sub = re.findall('ctrmc(.*)\n',clshowsrv)
        ctrmc_sub = ctrmc_sub[0].strip()
        ctrmc_state = re.findall('[a-z]*$',ctrmc_sub)
        ctrmc_state = ctrmc_state[0]
        ctrmc_dict = {'name':Ctrmc Subsystem,'state':ctrmc_state}
        # Get the ClstrmgrES Subsystem state
        clstrmgrES_sub = re.findall('clstrmgrES(.*)\n',clshowsrv)
        clstrmgrES_sub = clstrmgrES_sub[0].strip()
        clstrmgrES_state = re.findall('[a-z]*$',clstrmgrES_sub)
        clstrmgrES_state = clstrmgrES_state[0]
        clstrmgrES_dict = {'name':ClevmgrdES Subsystem,\
            'state':clstrmgrES_state}
        # Get the ClevmgrdES Subsystem state
        clevmgrdES_sub = re.findall('clevmgrdES(.*)\n',clshowsrv)
        clevmgrdES_sub = clevmgrdES_sub[0].strip()
        clevmgrdES_state = re.findall('[a-z]*$',clevmgrdES_sub)
        clevmgrdES_state = clevmgrdES_state[0]
        clevmgrdES_dict = {'name':ClevmgrdES Subsystem,\
            'state':clevmgrdES_state}
        # Get the ClinfoES Subsystem state
        clinfoES_sub = re.findall('clinfoES(.*)\n',clshowsrv)
        clinfoES_sub = clinfoES_sub[0].strip()
        clinfoES_state = re.findall('[a-z]*$',clinfoES_sub)
        clinfoES_state = clinfoES_state[0]
        clinfoES_dict = {'name':ClinfoES Subsystem,\
            'state':clinfoES_state}
        # Get the Clconfd Subsystem state
        clconfd_sub = re.findall('clconfd(.*)\n',clshowsrv)
        clconfd_sub = clconfd_sub[0].strip()
        clconfd_state = re.findall('[a-z]*$',clconfd_sub)
        clconfd_state = clconfd_state[0]
        clconfd_dict = {'name':Clconfd Subsystem,\
            'state':clconfd_state}
        # Get the Clcomd Subsystem state
        clcomd_sub = re.findall('clcomd(.*)\n',clshowsrv)
        clcomd_sub = clcomd_sub[0].strip()
        clcomd_state = re.findall('[a-z]*$',clcomd_sub)
        clcomd_state = clcomd_state[0]
        clcomd_dict = {'name':Clcomd Subsystem,\
            'state':clcomd_state}
        # Sort the data
        cls_status_lsit.extend([cluster_name_dict,cls_state_dict,\
            cls_substate_dict,cthags_dict,ctrmc_dict,\
            clstrmgrES_dict,clstrmgrES_dict,clevmgrdES_dict,\
            clconfd_dict,clcomd_dict])
        return cls_status_lsit
    # Get the node operating status
    def node_status(self):
        node_list_cmd = self.cmd_path + 'clmgr list node'
        node_list = os.popen(node_list_cmd)
        allnode_info_list = []
        for node in node_list:
            node_info_list = []
            node = node.strip()
            cldump_node_cmd = self.cmd_path + 'cldump |\
                sed \'/^$/d\'|sed \'/Node Name:/{x;p;x;}\'|\
                sed \'/Resource Group Name:/{x;p;x;}\'|\
                awk \'BEGIN{RS=""}{if ($3 == "'\
                + node +'")print $0}\''
            cldump_node_info = os.popen(cldump_node_cmd)
            cldump_node_info = cldump_node_info.read()
            # Get node name and state
            node_name = node
            node_state = re.findall('Node Name:(.*)\n',cldump_node_info)
            node_state = node_state[0].strip()
            node_state_dict = {'item':"Node Name",\
                'value':node_name,'state':node_state}
            node_info_list.append(node_state_dict)
            # Get Network Name and state
            network_list = re.findall('Network(.*)\n',cldump_node_info)
            for network in network_list:
                net_name = re.findall('Name:(.*)State',network)
                net_name = net_name[0].strip()
                net_state = re.findall('State:(.*)$',network)
                net_state = net_state[0].strip()
                net_state_dict = {'item':"Network Name",\
                    'name':net_name,'state':net_state}
                node_info_list.append(net_state_dict)
            # Get Address Name and state
            address_list = re.findall('(Address:.*)\n',cldump_node_info)
            for address in address_list:
                address_name = re.findall('(Address:.*)Label',address)
                address_name = address_name[0].strip()
                address_lable = re.findall('Label:(.*)State',address)
                address_lable = address_state[0].strip()
                address_state = re.findall('State:(.*)$',address)
                address_state = address_state[0].strip()
                address_state_dict = {'item':address_name,\
                    'name':address_lable,'state':address_state}
                node_info_list.append(address_state_dict)
            # Get node other status
            clshow_node_cmd = self.cmd_path + 'clshowsrv -v |\
                awk \'BEGIN{RS=""}{if ($3 == "\\"'\
                + node +'\\"")print $0}\''
            clshow_node_info = os.popen(clshow_node_cmd)
            clshow_node_info = clshow_node_info.read()
            # Get the node role
            node_role = re.findall('^([LR]?.*):',clshow_node_info)
            node_role = node_role[0].strip()
            # Get the Cluster services status
            cls_service = re.findall('Cluster services status:(.*)\n',\
                clshow_node_info)
            cls_service = cls_service[0].strip()
            cls_service_dict = {'item':node_role,\
                'name':'Cluster services','state':cls_service}
            node_info_list.append(cls_service_dict)
            # Get the Remote communications status
            remote_comm = re.findall('Remote communications:(.*)\n',\
                clshow_node_info)
            remote_comm = remote_comm[0].strip()
            remote_comm_dict = {'item':node_role,\
                'name':'Remote communications','state':cls_service}
            node_info_list.append(remote_comm_dict)
            # Get the Cluster-Aware AIX status
            cls_aware = re.findall('Cluster-Aware AIX status(.*)\n',\
                clshow_node_info)
            cls_aware = cls_aware[0].strip()
            cls_aware_dict = {'item':node_role,\
                'name':'Cluster-Aware AIX status','state':cls_aware}
            node_info_list.append(cls_aware_dict)
            allnode_info_list.append(node_info_list)
        return allnode_info_list
    # Get Resource Group information and status
    def rg_info(self):
        # Get the Resource Group name
        rg_list_cmd = self.cmd_path + 'clmgr list node'
        rg_list = os.popen(rg_list_cmd)
        allrg_info_list = []
        for rg in rg_list:
            rg = rg.strip()
            rg_info_list = []
            rg_name_dict = {'item':'Resource Group Name','value':rg}
            rg_info_list.append(rg_name_dict)
            rg_info_cmd = self.cmd_path + 'cldump |\
                sed \'/Resource Group Name:/{x;p;x;}\'|\
                awk \'BEGIN{RS=""}{if ($4 == "'\
                + rg + '")print $0}\''
            rg_info_list = os.popen(rg_info_cmd)
            rg_info = rg_info.read()
            # Get the Startup Policy
            startup_pol = re.findall('Startup Policy:(.*)\n',rg_info)
            startup_pol = startup_pol[0].strip()
            startup_pol_dict = {'name':'Startup Policy',\
                'value':startup_pol}
            rg_info_list.append(startup_pol_dict)
            # Get the Fallover Policy
            fallover_pol = re.findall('Fallover Policy:(.*)\n',rg_info)
            fallover_pol = fallover_pol[0].strip()
            fallover_pol_dict = {'name':'Fallover Policy',\
                'value':fallover_pol}
            rg_info_list.append(fallover_pol_dict)
            # Get the Fallback Policy
            fallback_pol = re.findall('Fallback Policy:(.*)\n',rg_info)
            fallback_pol = fallback_pol[0].strip()
            fallback_pol_dict = {'name':'Fallback Policy',\
                'value':fallback_pol}
            rg_info_list.append(fallback_pol_dict)
            # Get the Site Policy
            site_pol = re.findall('Site Policy:(.*)\n',rg_info)
            site_pol = site_pol[0].strip()
            site_pol_dict = {'name':'Site Policy','value':site_pol}
            rg_info_list.append(site_pol_dict)
            # Get the Participating Nodes Resource Group state
            node_rg_cmd = self.cmd_path + 'cldump |\
                sed \'/Resource Group Name:/{x;p;x;}\'|\
                awk \'BEGIN{RS=""}{if ($4 == "RG_ora")print $0}\'|\
                sed \'/--/G\'|\
                awk \'BEGIN{FS="\\n";RS=""}NR==2{print}\'|\
                awk \'{print $1,$2}\''
            node_rg_info = os.popen(node_rg_cmd)
            for node_rg in node_rg_info:
                node_rg = node_rg.strip()
                node_rg = node_rg.split(' ')
                node_rg_name = node_rg[0]
                node_rg_state = node_rg[1]
                node_rg_dict = {'name':node_rg_name,\
                    'value':node_rg_state}
                rg_info_list.append(node_rg_dict)
            allrg_info_list.append(rg_info_list)
        return allrg_info_list
