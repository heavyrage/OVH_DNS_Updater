#!/usr/bin/python

import urllib, re

sock = urllib.urlopen("http://monip.org/")
htmlSource = sock.read()
sock.close()

m = re.search('>IP : (.+?)<', htmlSource)
if m:
	found = m.group(1)
	msg="Current IP : "+found
	print msg
	f=open('/volume1/scripts/updateDNS/oldIP.txt','w')
	f.write(found)
	f.close()
