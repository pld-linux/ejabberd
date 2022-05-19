# TODO:
# - package all deps (tarballs 10-29) into separate spec files
#   (like in fedora)
# Conditional build:
%bcond_with	pam		# PAM authentication support
%bcond_with	logdb		# enable mod_logdb (server-side message logging)
%bcond_with	new_sql_schema	# build with the new SQL schema

Summary:	Fault-tolerant distributed Jabber/XMPP server
Summary(pl.UTF-8):	Odporny na awarie rozproszony serwer Jabbera/XMPP
Name:		ejabberd
Version:	22.05
Release:	1
License:	GPL
Group:		Applications/Communications
# Source0:	https://www.process-one.net/downloads/downloads-action.php?file=/%{version}/%{name}-%{version}.tar.gz
Source0:	https://github.com/processone/ejabberd/archive/refs/tags/%{version}.tar.gz
# Source0-md5:	4ebfd038cda9cb5ab34c95b49cff1bc8
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.service
Source4:	%{name}.logrotate

Source10:	ejabberd-base64url-20190617.tar.gz
# Source10-md5:	5a12fd2fb1f992c850aba5115aab3dd4
Source11:	ejabberd-cache_tab-20220502.tar.gz
# Source11-md5:	822bec23631e956ce927ecc5ae31e24d
Source12:	ejabberd-eimp-20220502.tar.gz
# Source12-md5:	39b7de8ad391da8fb12ff9b76301ced5
Source13:	ejabberd-elixir-20170515.tar.gz
# Source13-md5:	73be42f7d0cda7aeee5c0e6dadc0c451
Source14:	ejabberd-ezlib-20220502.tar.gz
# Source14-md5:	32dadbeff189a0fa18c21aa42258fa1a
Source15:	ejabberd-fast_tls-20220502.tar.gz
# Source15-md5:	1f341267a7d0bd953e961ccbe098e438
Source16:	ejabberd-fast_xml-20220502.tar.gz
# Source16-md5:	1288d6e5ea055784634367a0991adc3b
Source17:	ejabberd-fast_yaml-20220502.tar.gz
# Source17-md5:	1a513d2a074fc67678eecfbfc36c58b2
Source18:	ejabberd-idna-20180830.tar.gz
# Source18-md5:	e34174d5c5e2e91611d3249c690f6d2d
Source19:	ejabberd-jiffy-20220223.tar.gz
# Source19-md5:	b98489245dadf5a36ac3408be21d835a
Source20:	ejabberd-jose-20201223.tar.gz
# Source20-md5:	6e5c9910dc1e1894e31882d49f78967d
Source21:	ejabberd-mqtree-20220502.tar.gz
# Source21-md5:	1f1b175534eb917780e89e4c7d49c710
Source22:	ejabberd-p1_acme-20220502.tar.gz
# Source22-md5:	ada7344c8192e1999a73110ead29a704
Source23:	ejabberd-p1_mysql-20210721.tar.gz
# Source23-md5:	346f98e9eb7e098d91aef99af47ad3e3
Source24:	ejabberd-p1_oauth2-20220502.tar.gz
# Source24-md5:	bade7f8e1d18c9f6149b70268c73087b
Source25:	ejabberd-p1_pgsql-20220502.tar.gz
# Source25-md5:	052db14b243601591477abde6be1c74e
Source26:	ejabberd-p1_utils-20220502.tar.gz
# Source26-md5:	0eab972a4a247519e5a898d8da6054c1
Source27:	ejabberd-pkix-20220502.tar.gz
# Source27-md5:	88fd008dca6cf2208678fbf50b47a21a
Source28:	ejabberd-rebar_elixir_plugin-20160105.tar.gz
# Source28-md5:	6a069a566d71c3daa45fc4736364adf0
Source29:	ejabberd-sqlite3-20210721.tar.gz
# Source29-md5:	a81afbe7543f58fbb2cef732d73b3d3c
Source30:	ejabberd-stringprep-20220502.tar.gz
# Source30-md5:	721468fde880de8821c916c2534c9525
Source31:	ejabberd-stun-20220502.tar.gz
# Source31-md5:	27a002c7a5b3a6af6deb2a1eff281cfd
Source32:	ejabberd-unicode_util_compat-20170729.tar.gz
# Source32-md5:	1b348fdf38dba88ebed2f65125ad8590
Source33:	ejabberd-xmpp-20220502.tar.gz
# Source33-md5:	02378d906436ed5d5ece87419ff007ce
Source34:	ejabberd-yconf-20220502.tar.gz
# Source34-md5:	878e4993a860cc6384313e301b63a09b

Patch0:		%{name}-paths.patch
Patch1:		%{name}-config.patch
Patch2:		ejabberd-bug-3819.patch
# https://paleg.github.io/mod_logdb/
# https://github.com/paleg/ejabberd/compare/paleg:19.08...paleg:19.08-mod_logdb.patch
Patch3:		%{name}-mod_logdb.patch
URL:		http://www.ejabberd.im/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	erlang >= 2:22.2
BuildRequires:	expat-devel >= 1.95
BuildRequires:	openssl-devel
%if %{with pam}
BuildRequires:	pam-devel
%endif
BuildRequires:	git-core
BuildRequires:	rpmbuild(macros) >= 1.671
BuildRequires:	sqlite3-devel
BuildRequires:	yaml-devel
BuildRequires:	zlib-devel
Requires(post):	/usr/bin/perl
Requires(post):	jabber-common
Requires(post):	sed >= 4.0
Requires(post):	textutils
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	erlang >= 2:22.2
Requires:	expat >= 1.95
Requires:	rc-scripts
Requires:	systemd-units >= 38
Conflicts:	logrotate < 3.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprovfiles	%{_libdir}/%{name}/priv/lib/

%description
ejabberd is a Free and Open Source fault-tolerant distributed Jabber
server. It is written mostly in Erlang.

%description -l pl.UTF-8
ejabberd to darmowy, z otwartymi źródłami, odporny na awarie
rozproszony serwer Jabbera. Jest napisany w większości w Erlangu.

%package logdb
Summary:	Server-side logging module
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description logdb
Server-side logging module.

%prep
%setup -q -a 10 -a 11 -a 12 -a 13 -a 14 -a 15 -a 16 -a 17 -a 18 -a 19 -a 20 -a 21 -a 22 -a 23 -a 24 -a 25 -a 26 -a 27 -a 28 -a 29 -a 30 -a 31 -a 32 -a 33 -a 34
%patch2 -p1
%patch0 -p1
%patch1 -p1
%if %{with logdb}
%patch3 -p1
%endif

# Various parts of the build system use 'git describe'
# which returns nonsense on manual builds using the builder script
# and which fails on the PLD builders
# I was not able to locate all 'git describe' invocation, sot let's
# fool them with this dummy repository
unset GIT_DIR GIT_WORK_TREE
git init
git config user.email "dummy@example.com"
git config user.name "Dummy"
git add configure.ac
git commit -a -m "dummy commit"
git tag "%{version}"

sed -i -e 's,#!.*/usr/bin/env.*elixir,#!/usr/bin/elixir,' deps/elixir/bin/mix deps/elixir/lib/mix/lib/mix/tasks/escript.build.ex

%build
unset GIT_DIR GIT_WORK_TREE
%{__aclocal} -I m4
%{__autoconf}
%configure \
	%{?with_pam --enable-pam} \
	--enable-user=jabber \
 	%{__enable_disable new_sql_schema new-sql-schema} \
	--enable-elixir \
	--enable-full-xml \
	--enable-odbc \
	--enable-mysql \
	--enable-pgsql \
	--enable-sqlite --with-sqlite3 \
	%{?with_pam:--enable-pam} \
	--enable-zlib

touch deps/.got

cd deps/stringprep
%configure
cd ../..
cd deps/fast_tls
%configure
cd ../..
cd deps/fast_xml
%configure
cd ../..
cd deps/fast_yaml
%configure
cd ../..
cd deps/ezlib
%configure
cd ../..

# for elixir VM
LC_ALL=en_US.UTF-8; export LC_ALL
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/lib/%{name},/etc/{sysconfig,rc.d/init.d}} \
		$RPM_BUILD_ROOT{%{systemdunitdir},%{_sbindir}} \
		$RPM_BUILD_ROOT{/etc/logrotate.d,/var/log/archive/%{name}}

unset GIT_DIR GIT_WORK_TREE

%{__make} install -j1 \
	CHOWN_COMMAND=true \
	O_USER="" \
	G_USER="" \
	DESTDIR=$RPM_BUILD_ROOT

sed -e's,@libdir@,%{_libdir},g' -e 's,@EJABBERD_DOC_PATH@,%{_docdir}/%{name}-%{version}/doc,g' %{SOURCE1} > $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

chmod u+rw $RPM_BUILD_ROOT%{_sbindir}/%{name}*

chmod 755 $RPM_BUILD_ROOT%{_libdir}/*/priv/lib/*.so

rm -rf _doc 2>/dev/null || :
mv $RPM_BUILD_ROOT%{_docdir}/%{name} _doc

touch $RPM_BUILD_ROOT%{_sysconfdir}/jabber/ejabberd.cfg
touch $RPM_BUILD_ROOT/var/lib/ejabberd/.erlang.cookie

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -e /etc/jabber/ejabberd.cfg ] ; then
	%banner -e %{name} <<'EOF'
Old-style /etc/jabber/ejabberd.cfg configuration file exists. You should
consider converting it to the new YAML format. You can do this with the
'ejabberdctl convert_to_yaml' command (ejabberd must be already running).
EOF
fi

%post
if [ -f %{_sysconfdir}/jabber/secret ] ; then
	SECRET="$(cat %{_sysconfdir}/jabber/secret)"
	if [ -n "$SECRET" ] ; then
		echo -n "Updating component authentication secret in ejabberd config file..." >&2
		%{__sed} -i -e "s/@service_secret@/$SECRET/" /etc/jabber/ejabberd.yml
		echo "done" >&2
	fi
fi
/sbin/chkconfig --add ejabberd
if [ -e /var/run/%{name}-upgrade-trigger ] ; then
	# service will be restarted in the postun trigger
	rm -f /var/run/%{name}-upgrade-trigger || :
else
	%service ejabberd restart "ejabberd server"
	%systemd_post %{name}.service
fi

%preun
if [ "$1" = "0" ]; then
	%service ejabberd stop
	/sbin/chkconfig --del ejabberd
fi
%systemd_preun %{name}.service

%postun
%systemd_reload

%triggerprein -- %{name} < 13.10
if [ -e %{_sysconfdir}/jabber/ejabberd.cfg ] ; then
if grep -Eq '^[^%]*access_get' %{_sysconfdir}/jabber/ejabberd.cfg ; then
		echo "Your 'ejabberd.cfg' config file seems to use 'access_get' option of mod_vcard" >&2
		echo "this is not supported by this ejabberd version in PLD" >&2
		exit 1
	fi
rm -f %{_sysconfdir}/jabber/ejabberd.yml.rpmnew 2>/dev/null || :
fi
if [ -e /var/lock/subsys/ejabberd ] ; then
	# old init script won't stop ejabberd correctly
	# stop it's all processes here
	# we assume any 'epmd', 'beam', 'beam.smp' or 'heart' process
	# running with uid of jabber is ejabberd process
	pids="$(ps -C "epmd beam beam.smp heart" -o pid=,user= | awk '/jabber/ { print $1 }')" || :
	if [ -n "$pids" ] ; then
		%banner -e %{name} <<'EOF'
Killing all 'epmd, beam, beam.smp, heart' processed owned by the 'jabber' user to make sure old ejabberd is down.

EOF
		kill $pids || :
	fi
fi
touch /var/run/%{name}-upgrade-trigger || :

%triggerpostun -- %{name} < 13.10
# convert old 'NODENAME' in /etc/sysconfig/ejabberd
# to 'ERLANG_NODE' in /etc/jabber/ejabberdctl.cfg
# and move other settings
NODENAME="$(hostname)"
if [ -e /etc/sysconfig/ejabberd ] ; then
	. /etc/sysconfig/ejabberd || :
fi
subst="s/^#ERLANG_NODE=.*/ERLANG_NODE=ejabberd@${NODENAME}/"
if [ "$NODENAME" != "localhost" ] ; then
	%banner -e %{name} <<'EOF'
Configured node name (ejabberd@${NODENAME}) is not at 'localhost'.
– setting INET_DIST_INTERFACE=0.0.0.0 in /etc/jabber/ejabberdctl.cfg.
You should consider tuning that or your firewall configuration.

EOF
	subst="$subst;s/^#INET_DIST_INTERFACE=.*/INET_DIST_INTERFACE=0.0.0.0/"
fi
if [ -n "$ERL_MAX_PORTS" ] ; then
	subst="$subst;s/^#ERL_MAX_PORTS=.*/ERL_MAX_PORTS=${ERL_MAX_PORTS}/"
fi
sed -i -e"$subst" /etc/jabber/ejabberdctl.cfg || :
if [ -e /etc/sysconfig/ejabberd ] ; then
	sed -i.rpmsave \
		-e'/^[#[:space:]]*NODENAME=/d;/^# Node name/d' \
		-e'/^[#[:space:]]*ERL_MAX_PORTS=/d;/^# uncomment this to allow more then 1024 connections/d' \
		-e'/^[#[:space:]]*ERL_FULLSWEEP_AFTER=/d;/^# uncomment this to limit memory usage/d' \
		/etc/sysconfig/ejabberd || :
fi
cp %{_sysconfdir}/jabber/cookie /var/lib/ejabberd/.erlang.cookie || :
chown jabber:jabber /var/lib/ejabberd/.erlang.cookie || :
chmod 400 /var/lib/ejabberd/.erlang.cookie || :
if [ -e /etc/jabber/ejabberd.cfg -a ! -e /etc/jabber/ejabberd.yml.rpmnew ] ; then
	mv /etc/jabber/ejabberd.yml /etc/jabber/ejabberd.yml.rpmnew
	echo 'include_config_file: "/etc/jabber/ejabberd.cfg"' > /etc/jabber/ejabberd.yml || :
fi

# post action postponed here
%service ejabberd restart "ejabberd server"
%systemd_post %{name}.service

%systemd_trigger %{name}.service

%files
%defattr(644,root,root,755)
%doc sql _doc/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/elixir
%attr(755,root,root) %{_bindir}/iex
%attr(755,root,root) %{_bindir}/mix
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/ejabberd-inetrc
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/ejabberd.yml
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/ejabberdctl.cfg
# legacy config may still be there
%attr(640,root,jabber) %ghost %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/ejabberd.cfg
%attr(770,root,jabber) /var/log/%{name}
%attr(770,root,jabber) /var/log/archive/%{name}
%if %{with logdb}
%exclude %{_libdir}/ejabberd-%{version}/ebin/mod_logdb*
%endif
%{_libdir}/ejabberd-%{version}
%{_libdir}/base64url-*
%{_libdir}/cache_tab-*
%dir %{_libdir}/eimp-*
%dir %{_libdir}/eimp-*/priv
%dir %{_libdir}/eimp-*/priv/bin
%attr(755,root,root) %{_libdir}/eimp-*/priv/bin/eimp
%{_libdir}/eimp-*/ebin
%{_libdir}/eimp-*/LICENSE.txt
%{_libdir}/elixir-*
%{_libdir}/ezlib-*
%{_libdir}/fast_tls-*
%{_libdir}/fast_xml-*
%{_libdir}/fast_yaml-*
%{_libdir}/idna-*
%{_libdir}/jiffy-*
%{_libdir}/jose-*
%dir %{_libdir}/mqtree-*
%{_libdir}/mqtree-*/ebin
%dir %{_libdir}/mqtree-*/priv
%dir %{_libdir}/mqtree-*/priv/lib
%attr(755,root,root) %{_libdir}/mqtree-*/priv/lib/mqtree.so
%{_libdir}/p1_acme-*
%{_libdir}/p1_mysql-*
%{_libdir}/p1_oauth2-*
%{_libdir}/p1_pgsql-*
%{_libdir}/p1_utils-*
%dir %{_libdir}/pkix-*
%{_libdir}/pkix-*/ebin
%{_libdir}/pkix-*/LICENSE
%{_libdir}/rebar_elixir_plugin-*
%{_libdir}/sqlite3-*/ebin
%dir %{_libdir}/sqlite3-*
%dir %{_libdir}/sqlite3-*/priv
%attr(755,root,root) %{_libdir}/sqlite3-*/priv/sqlite3_drv.so
%{_libdir}/stringprep-*
%{_libdir}/stun-*
%{_libdir}/unicode_util_compat-*
%{_libdir}/xmpp-*
%{_libdir}/yconf-*
%dir %attr(770,root,jabber) /var/lib/ejabberd
%ghost %attr(400,jabber,jabber) %ghost %config(noreplace) %verify(not md5 mtime size) /var/lib/ejabberd/.erlang.cookie
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{systemdunitdir}/%{name}.service
/etc/logrotate.d/%{name}
%{_mandir}/man5/ejabberd.yml.5*

%if %{with logdb}
%files logdb
%defattr(644,root,root,755)
%{_libdir}/ejabberd-%{version}/ebin/mod_logdb*
%endif
