import fileinput
import os

for line in fileinput.input("/etc/haproxy/haproxy.cfg",inplace=True):
    if line.find('web2') > -1:
        s = line.find('web2') + 5
        s1 = line.find(':')
        fk = line[s:s1]
        print line.replace(fk, '10.139.148.231'),
        continue
    print line,

os.system('sudo service haproxy restart')
