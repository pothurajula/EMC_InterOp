import winreg
import sys
import HostParser

iscsi_path = r"SYSTEM\\CurrentControlSet\\Control\Class\\{4D36E97B-E325-11CE-BFC1-08002BE10318}"
fc_sas_path = r"SYSTEM\\CurrentControlSet\\Services\\mpio\\Parameters"
iscsi_path_timestamp = r"SYSTEM\\CurrentControlSet\\Services\\TCPIP\\Parameters"

def getDetails(host):
    topology, hostList = HostParser.getHost(host)
    return (topology, hostList)

def validateHost (host):
    try:
        access_registry = winreg.ConnectRegistry(host, winreg.HKEY_LOCAL_MACHINE)
        return (access_registry)
    except OSError:
        print("FAILURE..Please check connectivtiy with the host: ", host)
        return

def connectHostRegEdit(access_registry, path):
    mpio_access_key = winreg.OpenKey(access_registry, path, 0, winreg.KEY_ALL_ACCESS)
    return (mpio_access_key)

def getRegValue(key,param):
    value, type_= winreg.QueryValueEx(access_key, param)
    return value

def getCurrentRegistryValues(host,key,param,Output):
    with open(Output,"a+") as fd:
        fd.write("***************************************************************" +"\n")
        fd.write("Current registry Value are below for host: " + host +"\n")
        for index in range(len(param)):
            value = getRegValue(key, param[index])
            fd.write(param[index] +"="+ str(value)+"\n")
        fd.write("\n")

def setRegValue(key,param,value):
    winreg.SetValueEx(key,param,0,winreg.REG_DWORD,value)

def RegistryValueValidation(access_key, params, values):
    for index in range(len(params)):
        try:
            value = getRegValue(access_key, params[index])
            if value == values[index]:
                continue
            else:
                setRegValue(access_key, params[index], values[index])
        except:
            setRegValue(access_key, params[index], values[index])

def getiSCSIKeys(key, path):
    i = 0
    pathList=[]
    while True:
        try:
            sub_key = winreg.EnumKey(key, i)
            i += 1
            new_path = r"\\".join([path, sub_key])
            pathList.append(new_path)
        except WindowsError as e:
            break
    return (pathList)

def enableiSCSITimeStamp(access_registry, path):
    key = connectHostRegEdit(access_registry,path)
    setRegValue(key,"Tcp1323Opts",2)

if __name__ == "__main__":
    topology, hostList = getDetails("hosts.txt")
    with open("current_values.txt","w")as fd:
        pass
    for host in hostList:
        print ("*******************************************************************")
        print ("Currently setting values on host: ",host)
        access_registry= validateHost(host)
        if (access_registry):
            if (topology == "FC"):
                access_key = connectHostRegEdit(access_registry,fc_sas_path)
                parameters,values=HostParser.parseGoldenValues("FC_mpio_parameters.txt")
                RegistryValueValidation(access_key, parameters,values)
                getCurrentRegistryValues(host,access_key,parameters,"current_values.txt")
                print("Registry settings are updated and Current values are captured in the text file Current_values.txt ")
                winreg.CloseKey(access_key)
            elif (topology == "SAS"):
                access_key = connectHostRegEdit(access_registry,fc_sas_path)
                parameters,values=HostParser.parseGoldenValues("SAS_mpio_parameters.txt")
                RegistryValueValidation(access_key, parameters, values)
                getCurrentRegistryValues(host, access_key, parameters, "current_values.txt")
                print("Registry settings are updated and Current values are captured in the text file Current_values.txt ")
                winreg.CloseKey(access_key)
            elif (topology == "iSCSI"):
                access_key = connectHostRegEdit(access_registry,iscsi_path)
                parameters,values = HostParser.parseGoldenValues("iscsi_parameters.txt")
                pathList = getiSCSIKeys(access_key, iscsi_path)
                for path in pathList:
                    try:
                        key = connectHostRegEdit(access_registry, path)
                        value, type_ = winreg.QueryValueEx(key, "DriverDesc")
                        if (value == "Microsoft iSCSI Initiator"):
                            key = connectHostRegEdit(access_registry, path)
                            pathList = getiSCSIKeys(key, path)
                            for line in pathList:
                                if ("Parameters" in line):
                                    path=line
                            key = connectHostRegEdit(access_registry, path)
                            RegistryValueValidation(key, parameters, values)
                    except:
                       continue
                enableiSCSITimeStamp(access_registry, iscsi_path_timestamp)
                #getCurrentRegistryValues(host, access_key, parameters, "current_values.txt")
                print("Registry settings are updated and Current values are captured in the text file Current_values.txt ")
                winreg.CloseKey(access_key)
        else:
            continue

