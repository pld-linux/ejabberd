#!/bin/sh

umask 007 || exit $?
cd /var/lib/ejabberd || exit $?

COOKIE=`cat /etc/jabber/cookie`

COMMAND="setsid erl -pa @libdir@/ejabberd/ebin \
      -setcookie $COOKIE \
      -sname ejabberd \
      -s ejabberd \
      -ejabberd config \\\"/etc/jabber/ejabberd.cfg\\\" \
      log_path \\\"/var/log/ejabberd/ejabberd.log\\\" \
      -sasl sasl_error_logger \\{file,\\\"/var/log/ejabberd/sasl.log\\\"\\} \
      -kernel inetrc \\\"/etc/jabber/ejabberd-inetrc\\\" \
      -heart \
      -detached"

if [ "`id -u`" -eq "0" ] ; then
	exec su -s /bin/sh jabber -c "exec $COMMAND"
else
	eval "exec $COMMAND"
fi
