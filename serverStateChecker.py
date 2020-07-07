#!/usr/bin/python

from java.util import Date
from java.io import FileInputStream
import java.lang
import os
import string

propInputStream = FileInputStream("domain.properties")
configProps = Properties()
configProps.load(propInputStream)

adminUser = configProps.get("admin.username")
adminPassword = configProps.get("admin.password")
checkInterval = configProps.get("check.interval")
totalServersToMonitor = configProps.get("total.number.of.servers")
checkingIntervalSeconds = int(checkInterval)

print 'Checking All Servers State Details'
totalServers = int(totalServersToMonitor)
i=1
while i <= totalServers:
	disconnect()
	serverState=""
	serverName = configProps.get("server.name." + str(i))
	serverURL = configProps.get("server.url." + str(i))
	try:
		connect(adminUser,adminPassword,serverURL)
		serverRuntime()
		serverState=cmo.getState()
		print '-----------------', serverName , ' is in State: ', serverState
		if serverState != "RUNNING":
			today = Date()
			stateMessage = 'The ' + serverName + ' is In State ' + serverState + '  At Time: ' + today.toString()
			cmd = "echo " + stateMessage +" >> serverState_file"
			os.system(cmd)
	except:
		serverName=configProps.get("server.name." + str(i))
		print 'Sorry !!! Unable to Connect to Server ' , serverName
		today = Date()
		stateMessage = 'The ' + serverName + ' May Be DOWN.' + ' At Time: ' + today.toString()
		cmd = "echo " + stateMessage +" >> serverState_file"
		os.system(cmd)
	i =  i + 1
