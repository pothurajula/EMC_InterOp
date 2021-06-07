import winreg
import sys

iscsi_path = r"SYSTEM\\CurrentControlSet\\Control\Class\\{4D36E97B-E325-11CE-BFC1-08002BE10318}"
fc_sas_path = r"SYSTEM\\CurrentControlSet\\Services\\mpio\\Parameters"
iscsi_path_timestamp = r"SYSTEM\\CurrentControlSet\\Services\\TCPIP\\Parameters"

def getDetails():
    host_name = input("Enter the host name: ")
    host = host_name.strip()
    top_name = input("Enter the topology in format - FC/iSCSI/SAS: ")
    topology = top_name.strip()
    return (host, topology)

def validateHost (host):
    try:
        access_registry = winreg.ConnectRegistry(host, winreg.HKEY_LOCAL_MACHINE)
        return (access_registry)
    except:
        raise
        print("Please check connectivtiy with the host: ", host)
        sys.exit(1)

def connectHostRegEdit(access_registry, path):
    mpio_access_key = winreg.OpenKey(access_registry, path, 0, winreg.KEY_ALL_ACCESS)
    return (mpio_access_key)

def readFile(parameter_file):
    with open(parameter_file, "r+") as fd:
        data=fd.readlines()
        return (data)

def getRegValue(key,param):
    value, type_= winreg.QueryValueEx(access_key, param)
    return value

def setRegValue(key,param,value):
    winreg.SetValueEx(key,param,0,winreg.REG_DWORD,value)

def RegistryValueValidation(access_key, data):
    for line in data:
        x = line.strip().split("=")
        try:
            value = getRegValue(access_key, x[0])
            if value == int(x[1]):
                continue
            else:
                setRegValue(access_key, x[0], int(x[1]))
        except:
            setRegValue(access_key, x[0], int(x[1]))

def getiSCSIKeys(key):
    i = 0
    pathList=[]
    while True:
        try:
            sub_key = winreg.EnumKey(key, i)
            i += 1
            new_path = r"\\".join([iscsi_path, sub_key])
            pathList.append(new_path)
        except WindowsError as e:
            break
    return (pathList)

def enableiSCSITimeStamp(access_registry, path):
    #path = r"HKLM\SYSTEM\CurrentControlSet\Services\TCPIP\Parameters"
    #print (path)
    key = connectHostRegEdit(access_registry,path)
    setRegValue(key,"Tcp1323Opts",2)

if __name__ == "__main__":
    host,topology = getDetails()
    access_registry= validateHost(host)
    if (topology == "FC"):
        access_key = connectHostRegEdit(access_registry,fc_sas_path)
        parameters=readFile("FC_mpio_parameters.txt")
        RegistryValueValidation(access_key, parameters)
        winreg.CloseKey(access_key)
    elif (topology == "SAS"):
        access_key = connectHostRegEdit(access_registry,fc_sas_path)
        parameters=readFile("SAS_mpio_parameters.txt")
        RegistryValueValidation(access_key, parameters)
        winreg.CloseKey(access_key)
    elif (topology == "iSCSI"):
        access_key = connectHostRegEdit(access_registry,iscsi_path)
        parameters = readFile("iscsi_parameters.txt")
        pathList=getiSCSIKeys(access_key)
        for path in pathList:
            try:
                key= winreg.OpenKey(access_registry, path, 0, winreg.KEY_ALL_ACCESS)
                value, type_ = winreg.QueryValueEx(key, "DriverDesc")
                if (value == "Microsoft iSCSI Initiator"):
                    #print ("iscsi initiator found")
                    RegistryValueValidation(key, parameters)
            except:
               continue
        enableiSCSITimeStamp(access_registry, iscsi_path_timestamp)
        winreg.CloseKey(access_key)

