connect('urbancode','urbancode01!','t3://it005aia.it.sedc.internal.vodafone.com:7300')
x=ls('Servers',returnMap='true')
redirect("/opt/SP/weblogic/wlsadm/urbancode/agent/var/work//Middleware_Admin/ESB_PROD_MYVODAFONE/ServerStatus.log")
for i in x:
 state(i,'Server')
