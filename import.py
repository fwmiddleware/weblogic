from java.util import HashMap
from java.util import HashSet
from java.util import ArrayList
from java.io import FileInputStream
import getopt

from com.bea.wli.config import TypeIds
from com.bea.wli.sb.util import Refs
from com.bea.wli.config.customization import Customization
from com.bea.wli.sb.management.importexport import ALSBImportOperation

import sys

#=======================================================================================
# help
#=======================================================================================
def usage():
        print "NAME"
        print "\t import.py"
        print "\nSYNOPSIS"
        print "\timport.py [options]"
        print "\nDESCRIPTION"
        print "\tImport enterprice service bus configuration with customization file"
        print "\nFUNCTION LETTERS"
        print "\t-h, --help"
        print "\t\tthis help"
        print "\n\t-c, --conf [FILE NAME]"
        print "\t\tName of the jar configuration file (optional)."
        print "\n\t-s, --cust [CONFIGURATION FILE NAME]"
        print "\t\tName of the customization file (optional)."

#=======================================================================================
# load configuration file
#=======================================================================================
def loadConf(fileName):
        print "## Load configuration file ",fileName,"...",
        confProperties=Properties()
        try:
                confProperties.load(FileInputStream(fileName))
                print "OK!\n\n"
        except:
                print "FAILED!!!"
                print "error:"
                dumpStack();
                sys.exit(2)
        return confProperties

#=======================================================================================
# Connect to the Admin Server
#=======================================================================================
def connectToServer(username, password, url):
        print "# Try to connect to",url
        connect(username, password, url)
        domainRuntime()

#=======================================================================================
# find service in MBean tree
#=======================================================================================
def getService(name, type):
        #print "## Find service Name: ",name," type: ",type,"... ",
        service = findService(name, type)

        if service == None:
                print " MBean ",name," not found!!!"
                dumpStack()
                raise
        #else:
        #       print "OK!\n\n"

        return service

#=======================================================================================
# Utility function to create an arbitrary session name
#=======================================================================================
def createSessionName():
    sessionName = String("SessionScript"+Long(System.currentTimeMillis()).toString())
    return sessionName

#=======================================================================================
# connect to wl server
#=======================================================================================
def createSession(sessionName):

        # obtain session management mbean to create a session.
        # This mbean instance can be used more than once to
        # create/discard/commit many sessions

        sessionMBean = getService("Session","com.bea.wli.config.mbeans.SessionMBean")

        #print "## Try to create session " + sessionName + " ...",
        sessionMBean.createSession(sessionName)
        #print "OK!\n\n"

        return sessionMBean

#=======================================================================================
# read file
#=======================================================================================
def readBinaryFile(fileName):
        print "## Read file ",fileName,"... ",
        try:
                file=open(fileName,"rb")
        except:
                print "FAILED!!!"
                dumpStack()
                raise

        print "OK!\n"
        return file.read()


#=======================================================================================
# upload jar
#=======================================================================================
def upladJar(ALSBConfigurationMBean, jarFileName):
        print
        print "# Tryng to upload file",jarFileName
        try:
                theBytes=readBinaryFile(jarFileName)
                ALSBConfigurationMBean.uploadJarFile(theBytes)
                print "File uploaded!"
        except:
                print "FAILED!!!"
                print "Error during importing file",jarFileName
                dumpStack()
                sys.exit(2)

#=======================================================================================
# get configuration bean
#=======================================================================================
def getConfigurationBean(sessionName):
        try:
                ALSBConfigurationMBean = getService(String("ALSBConfiguration.").concat(sessionName),"com.bea.wli.sb.management.configuration.ALSBConfigurationMBean")
                return ALSBConfigurationMBean
        except:
                print "FAILED!!!"
                print "Error during get configuration bean"
                dumpStack()
                sys.exit(2)

#=======================================================================================
# Import Jar
#=======================================================================================
def importJar(ALSBConfigurationMBean, passphrase):
        print
        print "# Tryng to import file"
        alsbJarInfo = ALSBConfigurationMBean.getImportJarInfo()
        alsbImportPlan = alsbJarInfo.getDefaultImportPlan()
        alsbImportPlan.setPassphrase(passphrase)
        operationMap=HashMap()
        operationMap = alsbImportPlan.getOperations()
        print
        print 'Default importPlan'
        printOpMap(operationMap)
        set = operationMap.entrySet()

        alsbImportPlan.setPreserveExistingEnvValues(true)

        #boolean
        abort = false
        #list of created ref
        createdRef = ArrayList()

        for entry in set:
                ref = entry.getKey()
                op = entry.getValue()
                #set different logic based on the resource type

                print "Import source:",ref

                type = ref.getTypeId
                if type == TypeIds.SERVICE_ACCOUNT_REF or type == TypeIds.SERVICE_PROVIDER_REF:
                        if op.getOperation() == ALSBImportOperation.Operation.Create:
                                print 'Unable to import a service account or a service provider on a target system', ref
                                abort = true
                        elif op.getOperation() == ALSBImportOperation.Operation.Create:
                                #keep the list of created resources
                                createdRef.add(ref)

        if abort == true :
                print 'This jar must be imported manually to resolve the service account and service provider dependencies'
                SessionMBean.discardSession(sessionName)
                raise

        print
        print 'Modified importPlan'
        printOpMap(operationMap)

        importResult = ALSBConfigurationMBean.importUploaded(alsbImportPlan)

        printDiagMap(importResult.getImportDiagnostics())

        if importResult.getFailed().isEmpty() == false:
                print 'One or more resources could not be imported properly'
                raise

        print "# File imported!"
        return createdRef

#=======================================================================================
# Print customization
#=======================================================================================
def printCustomization(customization):
        if customization.__class__.__name__.find("FindAndReplaceCustomization")!=-1:
                query = customization.getQuery()
                print "\tReplace",query.getSearchString(),"with",customization.getReplacement(),"in:"
                for ref in customization.getTargets():
                        print "\t\t"+ref.toString()

        if customization.__class__.__name__.find("EnvValueCustomization")!=-1:
                print "\tSet follows enviroment values:"
                for ref in customization.getTargets():
                        print "\t\t"+ref.getFullName()
                print "\t\twith:"
                envList=customization.getEnvValues()

                for env in envList:
                        print env.getValue()

#=======================================================================================
# Import customization
#=======================================================================================
def importCustomization(customizationFile,ALSBConfigurationMBean,createdRef):
        if customizationFile != None:
                print
                print "# Tryng to import customization", customizationFile
                print 'Customization applied to the created resources only', createdRef
                iStream = FileInputStream(customizationFile)
                customizationList = Customization.fromXML(iStream)
                filteredCustomizationList = ArrayList()
                setRef = HashSet(createdRef)

                # apply a filter to all the customizations to narrow the target to the created resources
                for customization in customizationList:
                        filteredCustomizationList.add(customization)
                        printCustomization(customization)


                ALSBConfigurationMBean.customize(filteredCustomizationList)
                print "# customization file imported!"
        else:
                print
                print "# Customization file not specified!"


#=======================================================================================
# Utility function to print the list of operations
#=======================================================================================
def printOpMap(map):
    set = map.entrySet()
    for entry in set:
        op = entry.getValue()
        print op.getOperation(),
        ref = entry.getKey()
        print ref
    print

#=======================================================================================
# remove project
#=======================================================================================
def deleteProject(projectName,ALSBConfigurationMBean):
        print 'Deleting project',projectName,'...'
        refLocation = Refs()
        al = ArrayList()
        al.add(refLocation.makeLocationRef(projectName));
        ALSBConfigurationMBean.delete(al)

#=======================================================================================
# Utility function to print the diagnostics
#=======================================================================================
def printDiagMap(map):
    set = map.entrySet()
    for entry in set:
        diag = entry.getValue().toString()
        print diag
    print

def discardSession(session,sessionName):
        print
        print "# Discard session"
        session.discardSession(sessionName)

def commitSession(session,sessionName):
        print
        print "# Commit session"
        session.commitSession(sessionName)

def esb_import(argv):

        # property name constatnt
        PROPERTY_PROTOCOL="protocol"
        PROPERTY_HOST="host"
        PROPERTY_PORT="port"
        PROPERTY_USER="user"
        PROPERTY_PWD="pwd"
        PROPERTY_PROJECT="project"
        PROPERTY_PASSPHRASE="passphrase"
        PROPERTY_JAR_FILE="jarfile"
        PROPERTY_CUST_FILE="custfile"
        # ###########################

        connPropertiesFile=None
        projectPropertiesFile=None
        configurationFile=None
        customizationFile=None

        try:
                opts, args = getopt.getopt(argv, "hc:p:", ["help","conn=","project="])
        except getopt.GetoptError:
                print "Error during reading command line options"
                dumpStack();
                usage()
                sys.exit(2)

        for opt, arg in opts:

                print "opt:",opt,"arg:",arg

                if opt in ("-h", "--help"):
                        usage()
                        sys.exit()

                elif opt in ("-c","--conn"):
                        connPropertiesFile=arg

                elif opt in ("-p","--project"):
                        projectPropertiesFile=arg

        # reading configuration parameters
        connProperties=loadConf(connPropertiesFile)
        projectProperties=loadConf(projectPropertiesFile)

        passphrase=connProperties.get(PROPERTY_PASSPHRASE)
        project=projectProperties.get(PROPERTY_PROJECT)
        configurationFile=projectProperties.get(PROPERTY_JAR_FILE)
        customizationFile=projectProperties.get(PROPERTY_CUST_FILE)
        if customizationFile=="none":
                customizationFile=None

        print "--------------------------------------------------------"
        print "|                        actions summary               |"
        print "--------------------------------------------------------"
        print "| dddserver:\t\t\t|",connProperties.get(PROPERTY_PROTOCOL)+"://"+connProperties.get(PROPERTY_HOST)+":"+connProperties.get(PROPERTY_PORT)
        print "| project name:\t\t|",project
        print "| import file name:\t\t|",configurationFile
        print "| customization file name:\t|",customizationFile
        print "--------------------------------------------------------"
        print "\n"

        connectToServer(connProperties.get(PROPERTY_USER), connProperties.get(PROPERTY_PWD), connProperties.get(PROPERTY_PROTOCOL)+"://"+connProperties.get(PROPERTY_HOST)+":"+connProperties.get(PROPERTY_PORT))

        sessionName = createSessionName()
        sessionMbean = createSession(sessionName)

        ALSBConfigurationMBean = getConfigurationBean(sessionName)

        try:
                deleteProject(project,ALSBConfigurationMBean)
                commitSession(sessionMbean,sessionName)
        except:
                print "Error durin delete project",project
                dumpStack();
                discardSession(sessionMbean,sessionName)

        sessionName = createSessionName()
        sessionMbean = createSession(sessionName)
        ALSBConfigurationMBean = getConfigurationBean(sessionName)
        upladJar(ALSBConfigurationMBean, configurationFile)

        if project == None:
                print 'No project specified, additive deployment performed'
                importResult = ALSBConfigurationMBean.importUploaded(None, false, true, passphrase)
                sessionMbean.commitSession(sessionName)
        else:
                try:
                        createdRef = importJar(ALSBConfigurationMBean,passphrase)
                except:
                        print "Error during import jar File"
                        dumpStack();
                        discardSession(sessionMbean,sessionName)
                        sys.exit()

                try:
                        importCustomization(customizationFile,ALSBConfigurationMBean,createdRef)
                except:
                        print "Error durin import jar File"
                        dumpStack();
                        discardSession(sessionMbean,sessionName)
                        sys.exit()

                commitSession(sessionMbean,sessionName)


esb_import(sys.argv[1:])