uname = "appl_supp"
pwd = "vay7NAVe"
url = "t3://it005aia.it.sedc.internal.vodafone.com:7107"
from java.util import Date
t = Date()
def monitorThreadCount():
	connect(uname, pwd, url)
	serverRuntime()
	total = get("ThreadPoolRuntime/ThreadPoolRuntime/ExecuteThreadTotalCount")
	hogging = get("ThreadPoolRuntime/ThreadPoolRuntime/HoggingThreadCount")
	queue = get("ThreadPoolRuntime/ThreadPoolRuntime/QueueLength")
	idlecount = get("ThreadPoolRuntime/ThreadPoolRuntime/ExecuteThreadIdleCount")
	print t , ";  Total execute thread count is", total , ";  Hogging count is", hogging , ";  Queue length is", queue , ";  Idle Thread count is", idlecount
	
if __name__== "main":
	monitorThreadCount()
	exit()