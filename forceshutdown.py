import getopt, sys

opts, args = getopt.getopt(sys.argv[1:],'')
INSTANCE_URL = args[0]
print("DEBUG: instance url = " + INSTANCE_URL)
connect(url=INSTANCE_URL, userConfigFile='userfile.conf', userKeyFile='userfile.key')
shutdown(force='true')
exit()

