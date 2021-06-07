#!/usr/bin/python
import subprocess
import os
p=subprocess.check_output(['powershell.exe','Get-WmiObject Win32_PNPEntity | Select Name, DeviceID | Select-String PCI',],shell=True)
if p:
    print ("FC Available")
else:
    print ("Not FC")

"""with open("sample.txt", "r+") as gv:
    data=gv.readlines()
    for line in data:
        x=line.strip().split("=")
        print (x[0])"""