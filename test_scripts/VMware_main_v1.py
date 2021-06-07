import paramiko
import HostParser

cmd = " esxcli system module parameters list -m qlnativefc | grep ql2xmaxqdepth |  awk '{print $1,$3}'"
FC_cmd = "esxcli storage san fc list | grep \"Model Description\" | awk '{print $3}'"
Emulex_cmd = "esxcli system module parameters set -m lpfc -p \"lpfc_devloss_tmo=60 lpfc_lun_queue_depth=254\""

def connectHost(hostname, user, pwd):
    session = paramiko.SSHClient()
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print ("\nConnecting")
    session.connect(hostname, username = user, password = pwd)
    # ssh.connect('100.91.81.69', username='root', password='P@ssw0rd5')
    print("\nConnected")
    return (session)

def getFCAdapters(session, cmd):
    adapters = runCmd(session, cmd)
    FC_adapters = []
    for item in adapters:
        FC_adapters.append(item.strip())
    return (set(FC_adapters))

def runCmd(session, cmd):
    stdin, stdout, stderr = session.exec_command(cmd)
    output = stdout.readlines()
    return output

def setEmulexValues (session, Emulex_cmd):
    return (runCmd(session, Emulex_cmd))

##Supported -OutputFormat Text, XML, none
if __name__ == "__main__":
    topology, hostList = HostParser.getHost("VMWare_hosts.txt")
    for host in hostList:

    session = connectHost(h,'root','P@ssw0rd5')
    FCAdapters = getFCAdapters(session, FC_cmd)
    print ("FC Adapter present in the server:" ,FCAdapters)
    qlogic_values, emulex_values = HostParser.VMwareGoldenValues("VMware_FC_Parameters.txt")
    for adapter in FCAdapters:
        if (adapter == "Emulex"):
            output = setEmulexValues(session, Emulex_cmd)
        """elif (adapter == "Qlogic"):
            cmd = "esxcli system module parameters set -m qlnativefc -p \"ql2xmaxqdepth=255 ql2xloginretrycount=60 qlport_down_retry=60\""
            stdin, stdout, stderr = session.exec_command(cmd)
            output = stdout.readlines()
            print(output)"""
