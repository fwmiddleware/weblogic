connect('appl_supp','vay7NAVe','t3://10.252.98.12:7500')
domainRuntime()
cd('ServerRuntimes')
servers=domainRuntimeService.getServerRuntimes()
for server in servers:
  serverName=server.getName();
  print 'WLSserver', serverName , server.getState() , server.getHealthState()
print '**********************************************************'
cd('/')
cd('ServerRuntimes')
servers=domainRuntimeService.getServerRuntimes()
for server in servers:
  wls=server.getName();
  nameHost=server.getListenAddress();
  cd(wls+'/ThreadPoolRuntime/ThreadPoolRuntime')
  print 'ThreadTotalCount' , nameHost , wls , get('ExecuteThreadTotalCount')
  cd('../../..')
print '**********************************************************'
for server in servers:
  wls=server.getName();
  nameHost=server.getListenAddress();
  cd(wls+'/JVMRuntime/'+wls)
  HeapSizeCurrent=get('HeapSizeCurrent')/1048576
  HeapFreeCurrent=get('HeapFreeCurrent')/1048576
  HeapSizeMax=get('HeapSizeMax')/1048576
  HeapFreePercent=get('HeapFreePercent')
  HeapUsageCurrent=HeapSizeCurrent-HeapFreeCurrent
  print 'HeapSize' , nameHost ,  wls , HeapSizeCurrent, HeapFreeCurrent, HeapSizeMax, HeapFreePercent, HeapUsageCurrent
  cd('../../..')
print '**********************************************************'
for server in servers:
  wls=server.getName();
  nameHost=server.getListenAddress();
  jdbcDSrcs=server.getJDBCServiceRuntime().getJDBCDataSourceRuntimeMBeans()
  for jdbaDSrc in jdbcDSrcs:
    jdbcConnection=jdbaDSrc.getName()
    status=jdbaDSrc.getState()
    high=jdbaDSrc.getCurrCapacityHighCount()
    now =jdbaDSrc.getCurrCapacity()
    serverConfig()
    cd('/JDBCSystemResources/'+jdbcConnection+'/JDBCResource/'+jdbcConnection+'/JDBCConnectionPoolParams/'+jdbcConnection)
    maxCapacity=get('MaxCapacity')
    timeOut=get('InactiveConnectionTimeoutSeconds')
    print 'ConnetionPool', nameHost, wls ,jdbcConnection , status , now, high , maxCapacity, timeOut
    domainRuntime()
disconnect()




