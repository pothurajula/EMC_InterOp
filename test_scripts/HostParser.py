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
    topology = host[0]
    return (topology, host[1:])


