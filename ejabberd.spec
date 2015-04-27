
# Conditional build:
%bcond_with	pam		# PAM authentication support
%bcond_without	logdb		# enable mod_logdb (server-side message logging)
%bcond_with	weaker_crypto	# enable SSLv3

Summary:	Fault-tolerant distributed Jabber/XMPP server
Summary(pl.UTF-8):	Odporny na awarie rozproszony serwer Jabbera/XMPP
Name:		ejabberd
Version:	15.04
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	http://www.process-one.net/downloads/ejabberd/%{version}/%{name}-%{version}.tgz
# Source0-md5:	0a914f14ccb7f2d0a45e641efed21afd
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.service
Source4:	%{name}.logrotate
#
# Archives created with the ejabberd-pack_deps.sh script (in this repo)
Source10: ejabberd-ehyperloglog-20131012.tar.gz
# Source10-md5:	2cfc1b3aa27657093561a0db353729ef
Source11: ejabberd-elixir-20150414.tar.gz
# Source11-md5:	4d8051174896753120d908350afde614
Source12: ejabberd-esip-20150417.tar.gz
# Source12-md5:	c423d6e3239e61c4ad33a51d42d76ab2
Source13: ejabberd-goldrush-20140123.tar.gz
# Source13-md5:	6bc03a399ccffa90e28e5652281311de
Source14: ejabberd-jiffy-20150203.tar.gz
# Source14-md5:	2eba276e4020db79c671ca5a8579e98d
Source15: ejabberd-lager-20150212.tar.gz
# Source15-md5:	ddb1d51fc4571d29670658d00770a75f
Source16: ejabberd-p1_cache_tab-20150331.tar.gz
# Source16-md5:	bd6c7e0514dd25821c8aa3999d091357
Source17: ejabberd-p1_iconv-20150406.tar.gz
# Source17-md5:	4a9a767814bcc7ee6270b9a3565c56b4
Source18: ejabberd-p1_mysql-20150204.tar.gz
# Source18-md5:	5154bc83d3a2fb48f39758c95d2877bc
Source19: ejabberd-p1_pgsql-20150204.tar.gz
# Source19-md5:	3d9c26bee05e6ebf242406291ec6018c
Source20: ejabberd-p1_stringprep-20150204.tar.gz
# Source20-md5:	1a74552cf7be8cb17389a36cb8730f0b
Source21: ejabberd-p1_stun-20150404.tar.gz
# Source21-md5:	375244720bf70a8c0ebd0a05f16500b6
Source22: ejabberd-p1_tls-20150406.tar.gz
# Source22-md5:	e688514472cce3045f5c35836b4871e2
Source23: ejabberd-p1_utils-20150204.tar.gz
# Source23-md5:	aa9c8d70730498b2476bff018a6dc8ef
Source24: ejabberd-p1_xml-20150415.tar.gz
# Source24-md5:	7cc0d484fa53705ac18509da38e0cd84
Source25: ejabberd-p1_yaml-20150204.tar.gz
# Source25-md5:	72a7a6b865b93acdb2d21a3e928bebd7
Source26: ejabberd-p1_zlib-20150223.tar.gz
# Source26-md5:	de707b3a2309870165f0b5949d5f5dd1
Source27: ejabberd-rebar_elixir_plugin-20150420.tar.gz
# Source27-md5:	190e4578840a44d4a790b9be92fc345c
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
%setup -q -a 10 -a 11 -a 12 -a 13 -a 14 -a 15 -a 16 -a 17 -a 18 -a 19 -a 20 -a 21 -a 22 -a 23 -a 24 -a 25 -a 26 -a 27
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
	--enable-nif \
	--enable-odbc \
	--enable-mysql \
	--enable-pgsql \
	%{?with_pam:--enable-pam} \
	--enable-zlib \
	--enable-json \
	--enable-iconv \
	--enable-lager

touch deps/.got

cd deps/p1_iconv
%configure
cd ../..
cd deps/p1_stringprep
%configure
cd ../..
cd deps/p1_tls
%configure
cd ../..
cd deps/p1_xml
%configure \
	--enable-nif \
	--enable-full-xml
cd ../..
cd deps/p1_yaml
%configure
cd ../..
cd deps/p1_zlib
%configure
cd ../..
cd deps/esip
%configure
cd ../..

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

chmod 755 $RPM_BUILD_ROOT%{_libdir}/ejabberd/priv/lib/*.so

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
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/ejabberd-inetrc
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/ejabberd.yml
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/ejabberdctl.cfg
# legacy config may still be there
%attr(640,root,jabber) %ghost %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/ejabberd.cfg
%attr(770,root,jabber) /var/log/%{name}
%attr(770,root,jabber) /var/log/archive/%{name}
%if %{with logdb}
%exclude %{_libdir}/ejabberd/ebin/mod_logdb*
%endif
%{_libdir}/ejabberd
%dir %attr(770,root,jabber) /var/lib/ejabberd
%ghost %attr(400,jabber,jabber) %ghost %config(noreplace) %verify(not md5 mtime size) /var/lib/ejabberd/.erlang.cookie
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{systemdunitdir}/%{name}.service
/etc/logrotate.d/%{name}

%if %{with logdb}
%files logdb
%defattr(644,root,root,755)
%{_libdir}/ejabberd/ebin/mod_logdb*
%endif
