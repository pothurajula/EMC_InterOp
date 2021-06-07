import winreg

#for reading registry entries
access_registry = winreg.ConnectRegistry("benny.lab.beer.town",winreg.HKEY_LOCAL_MACHINE)
access_key = winreg.OpenKey(access_registry,r"SYSTEM\CurrentControlSet\Services\mpio\Parameters")
with open("mpio_parameters.txt","r+") as fd:
    data=fd.readlines()
    for line in data:
        x = line.strip().split("=")
        #print (x[0])
        value, type_= winreg.QueryValueEx(access_key, x[0])
        print (x[0] + ": ",value)
"""if value == 0:
    print("Retry Interval:\t", value)
else:
    winreg.SetValueEx(access_key, "RetryInterval", 0, winreg.REG_DWORD, 1)"""



