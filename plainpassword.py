from weblogic.security.internal import *  
from weblogic.security.internal.encryption import *

encryptionService = SerializedSystemIni.getEncryptionService(".")  
clearOrEncryptService = ClearOrEncryptedService(encryptionService)

passwd = raw_input("Enter encrypted password of one which you wanted to decrypt : ")

plainpwd = passwd.replace("\\", "")

print "Plain Text password is: " + clearOrEncryptService.decrypt(plainpwd)

### lanciare :
### source $DOMAIN_HOME/bin/setDomainEnv.sh
### java weblogic.WLST plainpassword.py