connect('urbancode','urbancode01!','t3://it005aia.it.sedc.internal.vodafone.com:7300')
domainRuntime()
cd('AppRuntimeStateRuntime/AppRuntimeStateRuntime')
AppList = cmo.getApplicationIds()
for App in AppList:
 print '#######',App ,' #######', cmo.getIntendedState(App)
disconnect()
exit()
