#
# TODO:
#	- config migration from old versions
#	- check/udpate the init script
#	- add systemd unit

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
Source3:	%{realname}.sh
Source4:	%{realname}ctl.sh
Source5:	%{realname}-inetrc
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
Patch0:		%{realname}-makefile.patch
# not available for 13.10
#Patch1:		%{realname}-vcard-access-get.patch
# http://www.dp.uz.gov.ua/o.palij/mod_logdb/patch-mod_logdb-2.1.12.diff
Patch2:		%{realname}-mod_logdb.patch
URL:		http://www.ejabberd.im/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	erlang >= 1:R15B01
BuildRequires:	expat-devel >= 1.95
BuildRequires:	openssl-devel
%if %{with pam}
BuildRequires:	pam-devel
%endif
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	yaml-devel
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
Summary:	Server-side logging module
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description logdb
Server-side logging module.

%prep
%setup -q -a 10 -a 11 -a 12 -a 13 -a 14 -a 15 -a 16 -a 17 -a 18 -a 19 -a 20 -a 21 -a 22 -a 23 -a 24
%patch0 -p1
#%%patch1 -p1
%if %{with logdb}
%patch2 -p0
%endif

%build
%{__aclocal} -I m4
%{__autoconf}
%configure \
	%{?with_pam --enable-pam} \
	--with-openssl=%{_prefix} \
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
install -d $RPM_BUILD_ROOT{/var/lib/%{realname},/etc/{sysconfig,rc.d/init.d},%{_sbindir}}

%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

sed -e's,@libdir@,%{_libdir},g' -e 's,@EJABBERD_DOC_PATH@,%{_docdir}/%{name}-%{version}/doc,g' %{SOURCE1} > $RPM_BUILD_ROOT/etc/rc.d/init.d/%{realname}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{realname}

chmod u+rw $RPM_BUILD_ROOT%{_sbindir}/%{realname}*
sed -e's,@libdir@,%{_libdir},g' %{SOURCE3} > $RPM_BUILD_ROOT%{_sbindir}/%{realname}
sed -e's,@libdir@,%{_libdir},g' %{SOURCE4} > $RPM_BUILD_ROOT%{_sbindir}/%{realname}ctl
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/jabber

chmod 755 $RPM_BUILD_ROOT%{_libdir}/ejabberd/priv/lib/*.so

rm -rf _doc 2>/dev/null || :
mv $RPM_BUILD_ROOT%{_docdir}/%{name} _doc

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -e /etc/jabber/ejabberd.cfg ] ; then
	if grep -Eq '^[^#]*access_get' ; then
		echo "Your 'ejabberd.cfg' config file seems to use 'access_get' option of mod_vcard" >&2
		echo "this is not supported by this ejabberd version in PLD" >&2
		exit 1
	fi
fi

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
%doc sql _doc/*
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
