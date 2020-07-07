#!/usr/bin/ksh

SCRIPT=$1

CWD=`pwd`
DOMAIN_DIR=$2

# Java parameters to launch WLST:
WLST_J_PAR="-client -Xms8m -Xmx64m -Xss1m -Dpython.cachedir=$HOME/wlstTemp"

. $DOMAIN_DIR/bin/setDomainEnv.sh
cd $CWD
$JAVA_HOME/java $WLST_J_PAR weblogic.WLST $SCRIPT


