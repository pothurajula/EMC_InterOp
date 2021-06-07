import winreg
access_registry = winreg.ConnectRegistry("samus.lab.beer.town", winreg.HKEY_LOCAL_MACHINE)
iscsi_path= r"SYSTEM\\CurrentControlSet\\Control\Class\\{4D36E97B-E325-11CE-BFC1-08002BE10318}"
fc_sas_path=r"SYSTEM\\CurrentControlSet\\Services\\mpio\\Parameters"

def connectHost(access_registry,path):
    #access_registry = winreg.ConnectRegistry(host, winreg.HKEY_LOCAL_MACHINE)
    mpio_access_key = winreg.OpenKey(access_registry,path,0, winreg.KEY_ALL_ACCESS)
    return (mpio_access_key)

def getKeys(access_key):
    i=0
    while True:
        try:
            sub_key=winreg.EnumKey(access_key, i)
            #print (sub_key)
            i += 1
            #new_path = iscsi_path + r"\\" + sub_key.strip()
            new_path= r"\\".join([iscsi_path, sub_key])
            key = connectHost(access_registry,new_path)
            #print ("After inside getkeys")
            #print (new_path)
            value, type_ = winreg.QueryValueEx(key, "DriverDesc")
            if (value == "Microsoft iSCSI Initiator"):
                print ("This is the iscsi initiator: ", sub_key)
        except WindowsError as e:
            #print ("No More items to list")
            break

access_key = connectHost(access_registry,iscsi_path)
getKeys(access_key)
