#
# Conditional build:
%bcond_with	pam		# PAM authentication support
%bcond_without	logdb		# enable mod_logdb (server-side message logging)
#

%define	realname	ejabberd

Summary:	Fault-tolerant distributed Jabber/XMPP server
Summary(pl.UTF-8):	Odporny na awarie rozproszony serwer Jabbera/XMPP
Name:		%{realname}
Version:	2.0.5
Release:	2
License:	GPL
Group:		Applications/Communications
Source0:	http://www.process-one.net/downloads/ejabberd/%{version}/%{realname}-%{version}.tar.gz
# Source0-md5:	2d85b47df969daf0a78ed3b16562d731
Source1:	%{realname}.init
Source2:	%{realname}.sysconfig
Source3:	%{realname}.sh
Source4:	%{realname}ctl.sh
Source5:	%{realname}-inetrc
Patch0:		%{realname}-makefile.patch
Patch1:		%{realname}-config.patch
Patch2:		%{realname}-mod_muc.patch
Patch3:		%{realname}-mod_logdb.patch
URL:		http://ejabberd.jabber.ru/
BuildRequires:	autoconf
BuildRequires:	erlang >= R10B_5
BuildRequires:	expat-devel >= 1.95
BuildRequires:	openssl-devel
%if %{with pam}
BuildRequires:	pam-devel
%endif
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires(post):	/usr/bin/perl
Requires(post):	jabber-common
Requires(post):	sed >= 4.0
Requires(post):	textutils
Requires(post,preun):	/sbin/chkconfig
Requires:	erlang
Requires:	expat >= 1.95
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ejabberd is a Free and Open Source fault-tolerant distributed Jabber
server. It is written mostly in Erlang.

%description -l pl.UTF-8
ejabberd to darmowy, z otwartymi źródłami, odporny na awarie
rozproszony serwer Jabbera. Jest napisany w większości w Erlangu.

%package logdb
Summary:        Server-side logging module
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description logdb
Server-side logging module.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%if %{with logdb}
%patch3 -p0
%endif

%build
cd src
%{__autoconf}
%configure \
	--enable-odbc %{?with_pam --enable-pam}
%{__make} -j1
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/lib/%{realname},/etc/{sysconfig,rc.d/init.d},%{_sbindir}}

%{__make} -C src install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

sed -e's,@libdir@,%{_libdir},g' -e 's,@EJABBERD_DOC_PATH@,%{_docdir}/%{name}-%{version}/doc,g' %{SOURCE1} > $RPM_BUILD_ROOT/etc/rc.d/init.d/%{realname}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{realname}

sed -e's,@libdir@,%{_libdir},g' %{SOURCE3} > $RPM_BUILD_ROOT%{_sbindir}/%{realname}
sed -e's,@libdir@,%{_libdir},g' %{SOURCE4} > $RPM_BUILD_ROOT%{_sbindir}/%{realname}ctl
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/jabber

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_sysconfdir}/jabber/secret ] ; then
	SECRET=`cat %{_sysconfdir}/jabber/secret`
	if [ -n "$SECRET" ] ; then
		echo "Updating component authentication secret in ejabberd config file..."
		%{__sed} -i -e "s/>secret</>$SECRET</" /etc/jabber/ejabberd.cfg
	fi
fi

if [ ! -f %{_sysconfdir}/jabber/cookie ] ; then
	echo "Generating erl authentication cookie..."
	umask 066
	perl -e 'open R,"/dev/urandom"; read R,$r,16;
		printf "%02x",ord(chop $r) while($r);' > %{_sysconfdir}/jabber/cookie
fi

/sbin/chkconfig --add ejabberd
%service ejabberd restart "ejabberd server"

%preun
if [ "$1" = "0" ]; then
	%service ejabberd stop
	/sbin/chkconfig --del ejabberd
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog doc src/odbc/pg.sql src/odbc/mysql.sql src/odbc/mssql.sql
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/*
%attr(770,root,jabber) /var/log/ejabberd
%if %{with logdb}
%exclude %{_libdir}/ejabberd/ebin/mod_logdb*
%endif
%{_libdir}/ejabberd
%dir %attr(770,root,jabber) /var/lib/ejabberd
%attr(754,root,root) /etc/rc.d/init.d/%{realname}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{realname}

%if %{with logdb}
%files logdb
%defattr(644,root,root,755)
%{_libdir}/ejabberd/ebin/mod_logdb*
%endif
