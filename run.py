from java.util import Date
from java.text import SimpleDateFormat
connect('appl_supp','vay7NAVe','t3://10.252.98.12:7500')
domainRuntime()
cd('ServerRuntimes')
cd('ESB_PROD_AGATHA_01')
strout=SimpleDateFormat('d MMM yyyy HH:mm:ss').format(java.util.Date(get('ActivationTime')))
print strout
