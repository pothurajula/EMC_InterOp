import socket

def getHost(filename):
    print (socket.gethostname())
    ignore = []
    host = []
    with open(filename,"r+") as fd:
        for line in fd:
            if not line.isspace():
                line=line.strip()
                if (line[0] == "#"):
                    ignore.append(line)
                else:
                    host.append(line)
    return (host)

host = getHost("hosts.txt")
print(host[1:])
topology = host[0]
print (topology)