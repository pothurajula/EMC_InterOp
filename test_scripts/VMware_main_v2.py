import paramiko
from paramiko.ssh_exception import BadHostKeyException

import HostParser
import sys

#cmd = " esxcli system module parameters list -m qlnativefc | grep ql2xmaxqdepth |  awk '{print $1,$3}'"
modulesCMDFC = "esxcli storage san fc list | grep \"Driver Name\""
modulesCMDSAS = "esxcli storage san sas list | grep \"Driver Name\""
VMware_FC_Params = "C:\\Users\\Administrator\\PycharmProjects\\PoC\\VMware\\VMware_FC_Params.txt"
VMware_SAS_Params = "C:\\Users\\Administrator\\PycharmProjects\\PoC\\VMware\\VMware_SAS_Params.txt"
VMware_iSCSI_Params = "C:\\Users\\Administrator\\PycharmProjects\\PoC\\VMware\\VMware_iSCSI_Params.txt"
PSP = "esxcli storage nmp satp rule add -s VMW_SATP_ALUA -V COMPELNT -P VMW_PSP_RR -o disable_action_OnRetryErrors -e \"Dell EMC SC Series Claim Rule\""

def connectHost(host, user, pwd):
    print ("Please Wait!!!!!. Establishing session to the host: ", host)
    try:
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(host, username = user, password = pwd)
        return (session)
    except paramiko.ssh_exception.AuthenticationException:
        print("Authentication failed, please verify your credentials provided for the host: ", host)
        return
    except paramiko.ssh_exception.SSHException:
        print("Unable to establish SSH connection. Please re-check connectivity and try again on host: ", host)
        return
    except:
        print("Error occured in connecting to the host. Please re-verify manual connection and try again on host: ", host)
        return

def getModules(session, cmd):
    modList = runCmd(session,cmd)
    modules = []
    for item in modList:
       if item.split(":")[1].strip() not in modules:
           modules.append(item.split(":")[1].strip())
    return (modules)

def getFCAdapters(session, cmd):
    adapters = runCmd(session, cmd)
    FC_adapters = []
    for item in adapters:
        FC_adapters.append(item.strip())
    return (set(FC_adapters))

def runCmd(session, cmd):
    stdin, stdout, stderr = session.exec_command(cmd)
    output = stdout.readlines()
    for line in output:
        if "Error" in line:
            print("Error encountered while running the command: ", cmd)
            sys.exit(1)
    return (output)

def setEmulexValues (session, module, params):
    cmd = "esxcli system module parameters set -m "+ module +" -p"
    interim_cmd= ""
    for key in params:
        interim_cmd = interim_cmd + key+ "=" + params[key] + " "
    cmd = cmd + " \""+interim_cmd + "\""
    return (runCmd(session, cmd))

def setQLogicValues (session, module, params):
    cmd = "esxcli system module parameters set -m qlnativefc -p"
    interim_cmd = ""
    for key in params:
        interim_cmd = interim_cmd + key + "=" + params[key] + " "
    cmd = cmd + " \"" + interim_cmd + "\""
    return (runCmd(session, cmd))

def setSASValues (session,module, params):
    cmd = "esxcli system module parameters set -p"
    interim_cmd= ""
    for key in params.keys():
        interim_cmd = interim_cmd + key+ "=" + params[key] + " "
    cmd = cmd + " \""+interim_cmd + "\"" + " -m " + module
    #print (cmd)
    return (runCmd(session, cmd))

def setiSCSIValues(session, hbaList,params):
    for hba in hbaList:
        for key in params.keys():
            cmd = "esxcli iscsi adapter param set -A=" + hba + " -k=" + key + " -v=" + params[key]
            print (runCmd(session,cmd))

if __name__ == "__main__":
    topology, hostList = HostParser.getHost("VMWare_hosts.txt")
    print ("Topology selected is: ", topology)
    print ("Lists of host on which the script will be run: ", hostList)
    with open("current_values.txt","w")as fd:
        pass
    for host in hostList:
        print("*******************************************************************")
        print("Script running on the host: ", host)
        session = connectHost(host,'root','P@ssw0rd5')
        if (session):
            if (topology == "FC"):
                modules = getModules(session, modulesCMDFC)
                qlogic_values, Emulex_values = HostParser.VMwareFCGoldenValues(VMware_FC_Params)
                print ("Modules that are in use are: ", modules)
                for module in modules:
                    if (module == "lpfc" or module == "lpfc820"):
                        print ("Parameters are being set for EMULEX")
                        result = setEmulexValues(session,module,Emulex_values)
                    elif (module == "qlnativefc"):
                        print ("Parameters are being set for Qlogic")
                        result = setQLogicValues(session,module, qlogic_values)
            elif (topology == "SAS"):
                modules = getModules(session, modulesCMDSAS)
                params = HostParser.GoldenValuesParser(VMware_SAS_Params)
                for module in modules:
                    if (module == "mpt3sas"):
                        print ("Module present is " + module + ". Hence retaining the default values only")
                    elif (module == "lsi_msgpt3"):
                        setSASValues(session,module,params)
            elif (topology == "SW_iSCSI"):
                hbacmd = " esxcli storage san iscsi list | grep \"Adapter: \" | awk '{print $2}'"
                output = runCmd(session, hbacmd)
                iscsiHBANum = []
                params = HostParser.GoldenValuesParser(VMware_iSCSI_Params)
                for hba in output:
                    iscsiHBANum.append(hba.strip())
                print ("iSCSI is configured on the HBA's: ", iscsiHBANum)
                setiSCSIValues(session, iscsiHBANum, params)
                moduleParamCmd = "esxcli system module parameters set -m iscsi_vmk -p iscsivmk_LunQDepth=255"
                runCmd(session, moduleParamCmd)
            print ("Setting the default path selection policy as: Round Robin")
            runCmd(session, PSP)
