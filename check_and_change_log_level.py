def conn_all():
    try:
        connect('appl_supp','vay7NAVe','t3://10.252.98.12:7100')
    except ConnectionException,e:
        print '\033[1;31m Unable to find admin server...\033[0m'
        exit()

def conn_web():
    try:
        connect('appl_supp','vay7NAVe','t3://10.252.98.11:7400')
    except ConnectionException,e:
        print '\033[1;31m Unable to find admin server...\033[0m'
        exit()

def conn_myvdf():
    try:
        connect('appl_supp','vay7NAVe','t3://10.252.98.11:7300') 
    except ConnectionException,e:
        print '\033[1;31m Unable to find admin server...\033[0m'
        exit()

def conn_merlino():
    try:
        connect('appl_supp','vay7NAVe','t3://10.252.98.12:7200') 
    except ConnectionException,e:
        print '\033[1;31m Unable to find admin server...\033[0m'
        exit()

def conn_agatha():
    try:
        connect('appl_supp','vay7NAVe','t3://10.252.98.12:7500')
    except ConnectionException,e:
        print '\033[1;31m Unable to find admin server...\033[0m'
        exit()

def current_log_level():
    try:
        print '   '
        print '##CURRENT LOG LEVEL ON DOMAIN##'
        print '   '
        i = 1
        status = ''
        LOG = ''
        a = ''
        print 'ESB_SERVER\t\t\t', 'LOG\t', 'STATE'
        serverNames = cmo.getServers()
        for name_server_to_check in serverNames:
          if i == 1:
            i = i + 1
          else:
            a= name_server_to_check.getName()
            cd('Servers/'+a+'/Log/'+a)
            LOG=cmo.getLogFileSeverity()
            cd('../../../../')
            status = status_server(a)
          print a+'\t\t' , LOG+'\t' , status
    except ConnectionException,e:
        print '\033[1;31m Unable to find admin server...\033[0m'
        exit()

def status_server(server):
    try:
        cd('/')
        domainRuntime()
        cd('ServerLifeCycleRuntimes/'+server)
        status = cmo.getState()
        cd('/')
        serverConfig()
        return status
    except ConnectionException,e:
        print '\033[1;31m Unable to find admin server...\033[0m'
        exit()



def update_log_level(newLogLelevel):
    try:
        print '   '
        print '#SYSTEM IS UPDATING LOG LEVEL ON DOMAIN##'
        print '   '
        i = 1
        serverNames = cmo.getServers()
	edit()
        startEdit()
        for name_server_to_check in serverNames:
          a= name_server_to_check.getName()
          cd('Servers/'+a+'/Log/'+a)
          if i == 1:
            i = i + 1
          else:
            cmo.setLogFileSeverity(newLogLelevel)
          cd('../../../../')
        save()
        activate()
    except ConnectionException,e:
        print '\033[1;31m Unable to find admin server...\033[0m'
        exit()


if __name__== "main":
    redirect('/opt/SP/weblogic/osb/SIMONE/CHECK_STATUS_LOG_LEVEL/Check.log', 'false')
    print 'SELECT DOMAIN:'
    print '   '
    print '1: ALL'
    print '2: WEB'
    print '3: MYVDF'
    print '4: MERLINO'
    print '5: AGATHA'
    print '6: EXIT'
    #print '0: Exit without changing log level'
    
    scelta = 0
    
    while (scelta == 0):
      try:
          scelta = input('Please, select domain by number:')
          if scelta == 1:
            print 'ALL'
            conn_all()
          elif scelta == 2:
            print 'WEB'
            conn_web()
          elif scelta == 3:
            print 'MYVDF'
            conn_myvdf()
          elif scelta == 4:
            print 'MERLINO'
            conn_merlino() 
          elif scelta == 5:
            print 'AGATHA'
	    conn_agatha()
          elif scelta == 6:
            exit() 
          else:
            print "Option not valid"
            scelta = 0
      except:
          scelta = 0
          print "Option not valid, only number" 
    current_log_level() 
    print '   '
    print '## NEW LOG LEVEL## '
    print '   '
    print 'SCEGLI IL NUOVO VALORE DI LOG LEVEL:'
    print '1: Debug'
    print '2: Info'
    print '3: Notice'
    print '4: EXIT without changing setting'
    #print '0: Exit without changing log level'
    
    scelta = 0
    
    while (scelta == 0):
      try:
          scelta = input('Inserisci una stringa:')
          if scelta == 1:
            print 'Debug'
            newLogLelevel='Debug'
          elif scelta == 2:
            print 'info'
            newLogLelevel='info'
          elif scelta == 3:
            print 'Notice'
            newLogLelevel='Notice'
          elif scelta == 4:
            disconnect()
            exit()            
          else:
            print "Scelta non valida"
            scelta = 0
      except:
          scelta = 0
    update_log_level(newLogLelevel)  
    current_log_level()
    disconnect()
    
 
