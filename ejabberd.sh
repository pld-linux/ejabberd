#!/bin/sh

umask 007 || exit $?
cd /var/lib/ejabberd || exit $?

COMMAND="setsid erl -pa /usr/lib/ejabberd/ebin \
      -sname ejabberd \
      -s ejabberd \
      -ejabberd config \\\"/etc/jabber/ejabberd.cfg\\\" \
      log_path \\\"/var/log/ejabberd/ejabberd.log\\\" \
      -sasl sasl_error_logger \\{file,\\\"/var/log/ejabberd/sasl.log\\\"\\} \
      -heart \
      -detached"

if [ "`id -u`" -eq "0" ] ; then
	exec su -s /bin/sh jabber -c "exec $COMMAND"
else
	eval "exec $COMMAND"
fi
