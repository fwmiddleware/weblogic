connect('weblogic','weblogic1','t3://10.246.40.77:9100')
domainRuntime()
cd('AppRuntimeStateRuntime/AppRuntimeStateRuntime')
#cd('ServerRuntimes')
#ls()
AppList = cmo.getApplicationIds()
print '####### Application #######  Application State\n'
print '***********************************************\n'
for App in AppList:
    print '#######',App ,' #######', cmo.getIntendedState(App)

print '***********************************************\n'