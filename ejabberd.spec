# TODO:
# - package all deps (tarballs 10-29) into separate spec files
#   (like in fedora)
# Conditional build:
%bcond_with	pam		# PAM authentication support
%bcond_without	logdb		# enable mod_logdb (server-side message logging)
%bcond_with	weaker_crypto	# enable SSLv3

Summary:	Fault-tolerant distributed Jabber/XMPP server
Summary(pl.UTF-8):	Odporny na awarie rozproszony serwer Jabbera/XMPP
Name:		ejabberd
Version:	16.12
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	http://www.process-one.net/downloads/ejabberd/%{version}/%{name}-%{version}.tgz
# Source0-md5:	fc571f0c0459860e876100ef1e1d225e
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.service
Source4:	%{name}.logrotate
#
# Archives created with the ejabberd-pack_deps.sh script (in this repo)
Source10: ejabberd-cache_tab-20161125.tar.gz
# Source10-md5:	2e249c108a599ba853e86ab1a7ad6425
Source11: ejabberd-elixir-20160606.tar.gz
# Source11-md5:	982db37dc8c8646a3053044dbdc7c030
Source12: ejabberd-esip-20161222.tar.gz
# Source12-md5:	5f1c5d6e87031f78cf5b901fbe012c50
Source13: ejabberd-ezlib-20160122.tar.gz
# Source13-md5:	295896d09211eba4d2c23f7f80c8ae7e
Source14: ejabberd-fast_tls-20161222.tar.gz
# Source14-md5:	1cfa0d5501c73d3e68849a0c87217cbc
Source15: ejabberd-fast_xml-20161125.tar.gz
# Source15-md5:	c56bbbf355bf6c9c0fb7a2f1df7dbd07
Source16: ejabberd-fast_yaml-20161125.tar.gz
# Source16-md5:	41771c5f3e45e2e2e91f426a89a53f47
Source17: ejabberd-goldrush-20151116.tar.gz
# Source17-md5:	5313eb34d8f4ab935307510c9c1c928d
Source18: ejabberd-iconv-20161125.tar.gz
# Source18-md5:	7e124d4f51703f994da6b7c5ae147213
Source19: ejabberd-jiffy-20160331.tar.gz
# Source19-md5:	96c2d7ef60375cf9c967d077be27678d
Source20: ejabberd-lager-20160610.tar.gz
# Source20-md5:	501e65b999507b3043741fbb31512fce
Source21: ejabberd-luerl-20151210.tar.gz
# Source21-md5:	22bd7e897cd41dd49623b0be698b9c5b
Source22: ejabberd-p1_mysql-20161125.tar.gz
# Source22-md5:	41ad1bf928ff160df1d9112da19de59f
Source23: ejabberd-p1_oauth2-20160123.tar.gz
# Source23-md5:	d16a2368fad6859e2fc4d93a15d4cd43
Source24: ejabberd-p1_pgsql-20161125.tar.gz
# Source24-md5:	446809132277766ba515deb24e0d547c
Source25: ejabberd-p1_utils-20161125.tar.gz
# Source25-md5:	1df40d68faecf5b546bc49b046ffde67
Source26: ejabberd-rebar_elixir_plugin-20160105.tar.gz
# Source26-md5:	3e9fcc00865d05472934d6eb414a2a1e
Source27: ejabberd-stringprep-20161125.tar.gz
# Source27-md5:	ec50b6b2b36f3db4d8fb8257e66309f8
Source28: ejabberd-stun-20161222.tar.gz
# Source28-md5:	116eeb16312cd788d6901b0e5fdc1509
Source29: ejabberd-xmpp-20161206.tar.gz
# Source29-md5:	7281f2bec8b4ec9bc9a21ee9a415ca2c
#
Patch0:		%{name}-paths.patch
Patch1:		%{name}-config.patch
# not available for 13.10
#Patch2:		%{name}-vcard-access-get.patch
# http://www.dp.uz.gov.ua/o.palij/mod_logdb/patch-mod_logdb-13.12.diff
Patch3:		%{name}-mod_logdb.patch
Patch4:		%{name}-no_sslv3_or_3des.patch
URL:		http://www.ejabberd.im/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	erlang >= 1:R16B03
BuildRequires:	expat-devel >= 1.95
BuildRequires:	openssl-devel
%if %{with pam}
BuildRequires:	pam-devel
%endif
BuildRequires:	rpmbuild(macros) >= 1.671
BuildRequires:	yaml-devel
BuildRequires:	zlib-devel
BuildRequires:	git-core
Requires(post):	/usr/bin/perl
Requires(post):	jabber-common
Requires(post):	sed >= 4.0
Requires(post):	textutils
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	erlang >= 1:R15B01
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
%setup -q -a 10 -a 11 -a 12 -a 13 -a 14 -a 15 -a 16 -a 17 -a 18 -a 19 -a 20 -a 21 -a 22 -a 23 -a 24 -a 25 -a 26 -a 27 -a 28 -a 29
%patch0 -p1
%patch1 -p1
#%%patch2 -p1
%if %{with logdb}
%patch3 -p1
%endif
%if %{without weaker_crypto}
%patch4 -p1
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

%build
unset GIT_DIR GIT_WORK_TREE
%{__aclocal} -I m4
%{__autoconf}
%configure \
	%{?with_pam --enable-pam} \
	--enable-user=jabber \
	--enable-elixir \
	--enable-full-xml \
	--enable-odbc \
	--enable-mysql \
	--enable-pgsql \
	%{?with_pam:--enable-pam} \
	--enable-zlib \
	--enable-iconv

touch deps/.got

cd deps/iconv
%configure
cd ../..
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
cd deps/esip
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
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service
install %{SOURCE4} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

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
if [ -e /etc/jabber/ejabberd.cfg ] ; then
	if grep -Eq '^[^%]*access_get' /etc/jabber/ejabberd.cfg ; then
		echo "Your 'ejabberd.cfg' config file seems to use 'access_get' option of mod_vcard" >&2
		echo "this is not supported by this ejabberd version in PLD" >&2
		exit 1
	fi
	rm -f /etc/jabber/ejabberd.yml.rpmnew 2>/dev/null || :
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
%{_libdir}/cache_tab-*
%{_libdir}/elixir-*
%{_libdir}/esip-*
%{_libdir}/ezlib-*
%{_libdir}/fast_tls-*
%{_libdir}/fast_xml-*
%{_libdir}/fast_yaml-*
%{_libdir}/goldrush-*
%{_libdir}/iconv-*
%{_libdir}/jiffy-*
%{_libdir}/lager-*
%{_libdir}/luerl-*
%{_libdir}/p1_mysql-*
%{_libdir}/p1_oauth2-*
%{_libdir}/p1_pgsql-*
%{_libdir}/p1_utils-*
%{_libdir}/rebar_elixir_plugin-*
%{_libdir}/stringprep-*
%{_libdir}/stun-*
%{_libdir}/xmpp-*
%dir %attr(770,root,jabber) /var/lib/ejabberd
%ghost %attr(400,jabber,jabber) %ghost %config(noreplace) %verify(not md5 mtime size) /var/lib/ejabberd/.erlang.cookie
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{systemdunitdir}/%{name}.service
/etc/logrotate.d/%{name}

%if %{with logdb}
%files logdb
%defattr(644,root,root,755)
%{_libdir}/ejabberd-%{version}/ebin/mod_logdb*
%endif
