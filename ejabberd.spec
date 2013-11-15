
# Conditional build:
%bcond_with	pam		# PAM authentication support
%bcond_with	logdb		# enable mod_logdb (server-side message logging)
#

%define	realname	ejabberd

Summary:	Fault-tolerant distributed Jabber/XMPP server
Summary(pl.UTF-8):	Odporny na awarie rozproszony serwer Jabbera/XMPP
Name:		%{realname}
Version:	13.10
Release:	0.1
License:	GPL
Group:		Applications/Communications
Source0:	http://www.process-one.net/downloads/ejabberd/%{version}/%{realname}-%{version}.tgz
# Source0-md5:	94ce4fe244ee72771eeafe27209d6d3c
Source1:	%{realname}.init
Source2:	%{realname}.sysconfig
Source3:	%{realname}.service
#
# Archives created with the ejabberd-pack_deps.sh script (in this repo)
Source10:	ejabberd-goldrush-20131108.tar.gz
# Source10-md5:	3f61708d20fcee2e7d47036cc470f4e9
Source11:	ejabberd-lager-20131111.tar.gz
# Source11-md5:	e0933da9d0462b045f6b9c4bbd320d3e
Source12:	ejabberd-p1_cache_tab-20130515.tar.gz
# Source12-md5:	f2500cffdaff434b354d01eeb24d136d
Source13:	ejabberd-p1_iconv-20130602.tar.gz
# Source13-md5:	ab0118d4097ee756f65fd087265c88ae
Source14:	ejabberd-p1_stringprep-20131113.tar.gz
# Source14-md5:	282d70c792a78ea9a7415b0b4e65e157
Source15:	ejabberd-p1_tls-20130717.tar.gz
# Source15-md5:	1211c5d8f0a95b58dfc5fb5bf4e13ded
Source16:	ejabberd-p1_xml-20131017.tar.gz
# Source16-md5:	dc7ebd7ed1ed6340ff0e7739173d4438
Source17:	ejabberd-p1_yaml-20131031.tar.gz
# Source17-md5:	82d4bb5c5d56ab93a60f5d1c6e583dc1
Source18:	ejabberd-p1_zlib-20130515.tar.gz
# Source18-md5:	a203d9359122ead64966eeb0bd1c8cf7
Source19:	ejabberd-xmlrpc-20130116.tar.gz
# Source19-md5:	22e02ff7ca174b4ac225005f63da10ad
Source20:	ejabberd-jiffy-20130702.tar.gz
# Source20-md5:	01b156e97005f07ce8bb46ecf27471ff
Source21:	ejabberd-p1_mysql-20131024.tar.gz
# Source21-md5:	c02921f21ba030357d2cbbbf182af54a
Source22:	ejabberd-p1_pam-20130515.tar.gz
# Source22-md5:	0ca31094d93dfb047f05c7539136433a
Source23:	ejabberd-p1_pgsql-20130515.tar.gz
# Source23-md5:	1958be8e59d1b472499ef1bdf8edc1db
Source24:	ejabberd-p1_stun-20130624.tar.gz
# Source24-md5:	9a1c5ad9b3b95364d3f76446fcf58dc3
#
Patch0:		%{realname}-paths.patch
Patch1:		%{realname}-config.patch
# not available for 13.10
#Patch2:		%{realname}-vcard-access-get.patch
# http://www.dp.uz.gov.ua/o.palij/mod_logdb/patch-mod_logdb-2.1.12.diff
Patch3:		%{realname}-mod_logdb.patch
URL:		http://www.ejabberd.im/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	erlang >= 1:R15B01
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
Requires:	erlang
Requires:	expat >= 1.95
Requires:	rc-scripts
Requires:	systemd-units >= 38
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
%setup -q -a 10 -a 11 -a 12 -a 13 -a 14 -a 15 -a 16 -a 17 -a 18 -a 19 -a 20 -a 21 -a 22 -a 23 -a 24
%patch0 -p1
%patch1 -p1
#%%patch2 -p1
%if %{with logdb}
%patch3 -p0
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
	--with-openssl=%{_prefix} \
	--enable-user=jabber \
	--enable-full-xml \
	--enable-nif \
	--enable-odbc \
	--enable-mysql \
	--enable-pgsql \
	%{?with_pam:--enable-pam} \
	--enable-zlib \
	--enable-stun \
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

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/lib/%{realname},/etc/{sysconfig,rc.d/init.d}} \
		$RPM_BUILD_ROOT{%{systemdunitdir},%{_sbindir}}

unset GIT_DIR GIT_WORK_TREE

%{__make} install -j1 \
	CHOWN_COMMAND=true \
	O_USER="" \
	G_USER="" \
	DESTDIR=$RPM_BUILD_ROOT

sed -e's,@libdir@,%{_libdir},g' -e 's,@EJABBERD_DOC_PATH@,%{_docdir}/%{name}-%{version}/doc,g' %{SOURCE1} > $RPM_BUILD_ROOT/etc/rc.d/init.d/%{realname}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{realname}
install %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service

chmod u+rw $RPM_BUILD_ROOT%{_sbindir}/%{realname}*

chmod 755 $RPM_BUILD_ROOT%{_libdir}/ejabberd/priv/lib/*.so

rm -rf _doc 2>/dev/null || :
mv $RPM_BUILD_ROOT%{_docdir}/%{name} _doc

touch $RPM_BUILD_ROOT%{_sysconfdir}/jabber/ejabberd.cfg
touch $RPM_BUILD_ROOT/var/lib/ejabberd/.erlang.cookie

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -e /etc/jabber/ejabberd.cfg ] ; then
	if grep -Eq '^[^#]*access_get' /etc/jabber/ejabberd.cfg ; then
		echo "Your 'ejabberd.cfg' config file seems to use 'access_get' option of mod_vcard" >&2
		echo "this is not supported by this ejabberd version in PLD" >&2
		exit 1
	fi
	%banner -e %{name} <<'EOF'
Old-style /etc/jabber/ejabberd.cfg configuration file exists. You should
consider converting it to the new YAML format. You can do this with the
ejabberctl command.
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
%service ejabberd restart "ejabberd server"

%systemd_post %{name}.service

%preun
if [ "$1" = "0" ]; then
	%service ejabberd stop
	/sbin/chkconfig --del ejabberd
fi
%systemd_preun %{name}.service

%postun
%systemd_reload

%triggerprein -- %{name} < 13.10
# only if started and we know upgrade won't be aborted in %%pre
if [ -e /var/lock/subsys/ejabberd ] && ! grep -Eq '^[^#]*access_get' /etc/jabber/ejabberd.cfg 2>/dev/null ; then
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

%triggerpostun -- %{name} < 13.10
# convert old 'NODENAME' in /etc/sysconfig/ejabberd
# to 'ERLANG_NODE' in /etc/jabber/ejabberdctl.cfg
# and move other settings
NODENAME="$(hostname)"
if [ -e /etc/sysconfig/ejabberd ] ; then
	. /etc/sysconfig/ejabberd || :
fi
subst="s/^#ERLANG_NODE=.*/ERLANG_NODE=ejabberd@${NODENAME}/"
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
%attr(770,root,jabber) /var/log/ejabberd
%if %{with logdb}
%exclude %{_libdir}/ejabberd/ebin/mod_logdb*
%endif
%{_libdir}/ejabberd
%dir %attr(770,root,jabber) /var/lib/ejabberd
%ghost %attr(400,jabber,jabber) %ghost %config(noreplace) %verify(not md5 mtime size) /var/lib/ejabberd/.erlang.cookie
%attr(754,root,root) /etc/rc.d/init.d/%{realname}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{realname}
%{systemdunitdir}/%{name}.service

%if %{with logdb}
%files logdb
%defattr(644,root,root,755)
%{_libdir}/ejabberd/ebin/mod_logdb*
%endif
