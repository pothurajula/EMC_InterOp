import winreg

host_name=input("Enter the host name or IP Addr: ")
hn=host_name.strip()
access_registry = winreg.ConnectRegistry(hn,winreg.HKEY_LOCAL_MACHINE)
access_key = winreg.OpenKey(access_registry,r"SYSTEM\CurrentControlSet\Services\mpio\Parameters",0, winreg.KEY_ALL_ACCESS)
with open("mpio_parameters.txt","r+") as fd:
    data=fd.readlines()
    for line in data:
        x = line.strip().split("=")
        try:
            value, type_ = winreg.QueryValueEx(access_key, x[0])
            #print ("TRY BLOCK VALUES BEFORE UPDATING: ",x[0] + ": ",value)
            if value == int(x[1]):
                continue
            else:
                winreg.SetValueEx (access_key,x[0],0, winreg.REG_DWORD,int(x[1]))
        except:
            #print ("EXCEPT BLOCK VALUE: " + x[0] + " is not present. Creating it below")
            winreg.SetValueEx (access_key,x[0],0, winreg.REG_DWORD,int(x[1]))
            value, type_ = winreg.QueryValueEx(access_key, x[0])
        finally:
            value, type_ = winreg.QueryValueEx(access_key, x[0])
            print ("FINAL BLOCK VALUES: ",x[0] + ": ",value)
            print ("----Please recheck the RetryInterval values on SAS systems----")
winreg.CloseKey(access_key)
