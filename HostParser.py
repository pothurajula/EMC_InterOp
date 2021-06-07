def getHost(filename):
    ignore = []
    host = []
    with open(filename, "r+") as fd:
        for line in fd:
            if not line.isspace():
                line = line.strip()
                if (line[0] == "#"):
                    ignore.append(line)
                else:
                    host.append(line)
    #topology = host[0]
    return (host)

def parseGoldenValues(parameter_file):
    with open(parameter_file, "r+") as fd:
        data=fd.readlines()
        parameter = []
        values = []
        for line in data:
            x = line.strip().split("=")
            parameter.append(x[0])
            values.append(int(x[1]))
    return (parameter,values)

def VMwareFCGoldenValues(parameter_file):
    with open(parameter_file, "r+") as fd:
        data=fd.readlines()
        #print (data)
        qlogic_values = { }
        emulex_values = { }
        values = { }
        for line in data:
            x = line.strip().split("=")
            if (x[0].startswith("ql")):
                qlogic_values[x[0]] = x[1]
            elif (x[0].startswith("lpfc")):
                emulex_values[x[0]] = x[1]
        return (qlogic_values, emulex_values)

def GoldenValuesParser(parameter_file):
    with open(parameter_file, "r+") as fd:
        data = fd.readlines()
        parameter_dict= {}
        for line in data:
            x = line.strip().split("=")
            parameter_dict[x[0]]=x[1]
        return (parameter_dict)


GoldenValuesParser("C:\\Users\\Administrator\\PycharmProjects\\PoC\\VMware\\VMware_SAS_Params.txt")


