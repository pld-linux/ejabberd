#!/bin/sh

cd /var/lib/ejabberd || exit $?

COMMAND="erl -pa @libdir@/ejabberd/ebin \
      -noinput \
      -sname ejabberdctl \
      -s ejabberd_ctl \
      -extra $@"

if [ "`id -u`" -eq "0" ] ; then
	exec su -s /bin/sh jabber -c "exec $COMMAND"
else
	eval "exec $COMMAND"
fi
