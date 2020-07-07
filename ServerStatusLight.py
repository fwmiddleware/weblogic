#!/usr/bin/python

from java.util import Date
from java.io import FileInputStream
import java.lang
import os
import string

propInputStream = FileInputStream("domain.properties")
configProps = Properties()
configProps.load(propInputStream)

username = configProps.get("admin.username")
password = configProps.get("admin.password")
URL = configProps.get("server.url.1")

connect(username,password,URL)
domainConfig()
serverList=cmo.getServers();
domainRuntime()


#cd('ServerRuntimes')

cd('ServerLifeCycleRuntimes')
for server in serverList:
            name=server.getName()
            cd(name)
            serverState=cmo.getState()
            print  name +' '+serverState
            cd('..')
