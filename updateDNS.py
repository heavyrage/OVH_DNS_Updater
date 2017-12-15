#!/usr/bin/python

import pprint
from SOAPpy import WSDL
import urllib
import re
import os.path
import datetime
import time

user=''
user_passwd=''
DOMAIN_NAME=''
SCRIPT_PATH=''
LOGFILE=SCRIPT_PATH+''

def mylogfile(text):
	lfile=LOGFILE
	now=datetime.datetime.now().time()
	tmp=now.strftime("%Y%m%d - %H:%M:%S - ")
	f=open(lfile,'a')
	f.write(tmp+text+"\n")
	f.close()
	print tmp+text

def initWSDL():
	soap = WSDL.Proxy('https://www.ovh.com/soapi/soapi-re-1.63.wsdl')
	return soap

def login(soap, user, passwd):

	#login
	session = soap.login(user, passwd, 'fr', 0)
	mylogfile("login successfull")
	return session

mylogfile("Starting script")

sock = urllib.urlopen("http://monip.org/")
htmlSource = sock.read()
sock.close()

m = re.search('>IP : (.+?)<', htmlSource)
if m:
	found = m.group(1)
	msg="Current IP : "+found
	mylogfile(msg)



oldIpFile=SCRIPT_PATH+'/oldIP.txt'
if os.path.isfile(oldIpFile):
	f=open(oldIpFile,'r')
	if f:
		oldIp=f.read()
	f.close()
else:
	mylogfile("No oldIP.txt file. Lookup for online entry.")
	
	soap=initWSDL()
	session=login(soap,user,user_passwd)
	#zoneEntryList
	result = soap.zoneEntryList(session, DOMAIN_NAME)
	mylogfile("zoneEntryList successfull")
	
	for i in xrange(len(result.item)):
		if result.item[i].fieldtype == 'A' and result.item[i].subdomain == '' :
			oldIp = result.item[i].target
			msg="Listed IP : "+oldIp
			mylogfile(msg)


if found <> oldIp and found:
	mylogfile("Old IP : "+oldIp)
	try:
		  session
	except NameError:
		soap=initWSDL()
		session=login(soap,user,user_passwd)
	else:
		mylogfile("Modifying online entry...")
	# zoneEntryModify
	soap.zoneEntryModify(session, 'heavyrage.ovh', '', 'A', oldIp, found)
	mylogfile("zoneEntryModify successfull")
	
	#logout
	soap.logout(session)
	mylogfile("logout successfull")

	mylogfile("Saving current IP.")
	f=open(oldIpFile,'w')
	f.write(found)
	f.close()
	soap.logout(session)
else :
	mylogfile("no need to update")

try:
	soap
except NameError:
	print ""
else:
	soap.logout(session)
	mylogfile("logout sucessfull")
	
