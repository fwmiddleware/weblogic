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

def current_state():
    try:
        i = 1
        status = ''
        LOG = ''
        a = ''
        time_start = ''
        serverNames = cmo.getServers()
        for name_server_to_check in serverNames:
          if i == 1:
            i = i + 1
          else:
            a= name_server_to_check.getName()
            status = status_server(a)
            time_start = started_time(a) 
          print a+'\t' , time_start+'\t' , status 
    except ConnectionException,e:
        print '\033[1;31m Unable to find admin server...\033[0m'
        exit()

def started_time(server):
    try:
        cd('/')
        domainRuntime()
        try:
            cd('ServerRuntimes/'+server)
            time_start=SimpleDateFormat('d MMM yyyy HH:mm:ss').format(java.util.Date(get('ActivationTime')))
        except:
            time_start = 'Not Available       '
        serverConfig()
        return time_start 
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

def quit():
    disconnect()


if __name__== "main":
    from java.util import Date
    from java.text import SimpleDateFormat
    redirect('/opt/SP/weblogic/osb/SIMONE/CHECK_STATE/Check.log', 'false')
    print 'SELECT DOMAIN:'
    print '   '
    print '1: ALL'
    print '2: WEB'
    print '3: MYVDF'
    print '4: MERLINO'
    print '5: AGATHA'
    print '6: VIEW_ALL_INSTANCES'
    print '7: EXIT'
    
    scelta = 0
    
    while (scelta == 0):
      try:
          scelta = input('Please, select domain by number:')
          if scelta == 1:
            print 'ALL'
            conn_all()
            current_state()
            quit()
          elif scelta == 2:
            print 'WEB'
            conn_web()
            current_state()
            quit()
          elif scelta == 3:
            print 'MYVDF'
            conn_myvdf()
            current_state()
            quit()
          elif scelta == 4:
            print 'MERLINO'
            conn_merlino()
            current_state()
            quit()
          elif scelta == 5:
            print 'AGATHA'
	    conn_agatha()
            current_state()
            quit()
          elif scelta == 6:
       	    conn_all()
            current_state()
            quit() 
	    conn_web()
            current_state()
            quit()
            conn_myvdf()
            current_state()
            quit()
            conn_merlino()
            current_state()
            quit()
            conn_agatha()
            current_state()
            quit()
          elif scelta == 7:
            exit() 
          else:
            print "Option not valid"
            scelta = 0
      except:
          scelta = 0
          print "Option not valid, only number" 
    
 
