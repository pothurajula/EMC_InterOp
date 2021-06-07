import winreg
#for writing new values to registries
#host_name=input("enter host name")
#hn=host_name.strip()
access_registry = winreg.ConnectRegistry(r"cabal.lab.beer.town",winreg.HKEY_LOCAL_MACHINE)
print ("Access_registry")
access_key = winreg.OpenKey(access_registry,r"SYSTEM\CurrentControlSet\Services\mpio\Parameters",0, winreg.KEY_ALL_ACCESS )
value, type_= winreg.QueryValueEx(access_key, "RetryInterval")
print (value)
#winreg.SetValueEx (access_key,"test",0, winreg.REG_DWORD,1)