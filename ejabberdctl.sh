#!/bin/sh

cd /var/lib/ejabberd || exit $?

COOKIE=`cat /etc/jabber/cookie`

COMMAND="erl -pa @libdir@/ejabberd/ebin \
      -setcookie $COOKIE \
      -noinput \
      -sname ejabberdctl \
      -s ejabberd_ctl \
      -extra $@"

if [ "`id -u`" -eq "0" ] ; then
	exec su -s /bin/sh jabber -c "exec $COMMAND"
else
	eval "exec $COMMAND"
fi
