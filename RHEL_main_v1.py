import connection
import HostParser

hbacmd= "lspci | grep -i fibre | awk '{print $4}'"

def qlportRetrytime(session):
    cmd = "cat \/sys\/module\/qla2xxx\/parameters\/qlport_down_retry"
    output = runCmd(session,cmd)
    return (output.pop())

def lpfcDevLosstmo(session):
    cmd = "cat \/sys\/module\/lpfc\/parameters\/lpfc_devloss_tmo"
    output = runCmd(session,cmd)
    return (output.pop())

def runCmd(session, cmd):
    stdin, stdout, stderr = session.exec_command(cmd)
    output = stdout.readlines()
    for line in output:
        if "Error" in line:
            print("Error encountered while running the command: ", cmd + "\n")
            pass
    return (output)

def getHBA(session,cmd):
    output = runCmd(session,cmd)
    adapters = []
    for item in output:
        if item.strip() not in adapters:
            adapters.append(item.strip())
    return (adapters)

def createQla2xxxConf(session):
    createCmd = "echo \"options qla2xxx qlport_down_retry=60\" > \/etc\/modprobe.d\/qla2xxx.conf"
    runCmd(session,createCmd)
    initRebuild(session)

def createlpfcconf(session):
    createCmd = "echo \"options lpfc lpfc_devloss_tmo=60\" > \/etc\/modprobe.d\/lpfc.conf"
    runCmd(session, createCmd)
    initRebuild(session)

def initRebuild(session):

    initrdcommands =["cp \/boot\/initramfs-$(uname -r).img \/boot\/initramfs-$(uname -r).img.bak",
                    "dracut -f"]
    print ("running dracut -f....")
    for cmd in initrdcommands:
        runCmd(session,cmd)
    print ("initrd rebuild. Rebooting the server....")
    runCmd(session,"reboot")

if __name__ == "__main__":
    hostList = HostParser.getHost("RHEL_hosts.txt")
    for host in hostList:
        print("*******************************************************************")
        print("Currently setting values on host: ", host)
        session = connection.connectHost(host,'root','password')
        if (session):
            adapterList = getHBA(session, hbacmd)
            print ("Adapters present in the " + host +" are:")
            for adapter in adapterList:
                print (adapter)
            for item in adapterList:
                if (item == "Emulex"):
                    lpfc_devloss_tmo=int(lpfcDevLosstmo(session))
                    if(lpfc_devloss_tmo == 60):
                        print ("lpfc_devloss_tmo is already set to 60.Hence proceeding to next host")
                    else:
                        print ("Configuring lpfc.conf file")
                        createlpfcconf(session)
                elif (item == "QLogic"):
                    retryTime = int(qlportRetrytime(session))
                    if (retryTime == 60):
                        print ("qlport down retry time is already set to 60. Hence proceeding to next host")
                        pass
                    else:
                        print ("Configuring qla2xxx.conf file")
                        createQla2xxxConf(session)
