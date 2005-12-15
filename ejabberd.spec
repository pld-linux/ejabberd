Summary:	Fault-tolerant distributed Jabber/XMPP server
Summary(pl):	Odporny na awarie rozproszony serwer Jabbera/XMPP
Name:		ejabberd
Version:	1.0.0
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	http://www.process-one.net/en/projects/ejabberd/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	bc0bfdad2e5e48e42fcc5d09384be74f
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.sh
Source4:	%{name}ctl.sh
Source5:	%{name}-inetrc
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-mod_muc.patch
URL:		http://ejabberd.jabberstudio.org/
BuildRequires:	autoconf
BuildRequires:	erlang >= R8B
BuildRequires:	expat-devel >= 1.95
BuildRequires:	openssl-devel
Requires(post):	/usr/bin/perl
Requires(post): jabber-common
Requires(post):	textutils
Requires(post,preun):	/sbin/chkconfig
Requires:	erlang
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ejabberd is a Free and Open Source fault-tolerant distributed Jabber
server. It is written mostly in Erlang.

%description -l pl
ejabberd to darmowy, z otwartymi �r�d�ami, odporny na awarie
rozproszony serwer Jabbera. Jest napisany w wi�kszo�ci w Erlangu.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd src
%{__autoconf}
%configure
%{__make}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/lib/%{name},/etc/{sysconfig,rc.d/init.d},%{_sbindir}}

%{__make} -C src install \
	DESTDIR=$RPM_BUILD_ROOT

sed -e's,@libdir@,%{_libdir},g' %{SOURCE1} > $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

sed -e's,@libdir@,%{_libdir},g' %{SOURCE3} > $RPM_BUILD_ROOT/%{_sbindir}/%{name}
sed -e's,@libdir@,%{_libdir},g' %{SOURCE4} > $RPM_BUILD_ROOT/%{_sbindir}/%{name}ctl
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/jabber

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/jabber/secret ] ; then
	SECRET=`cat /etc/jabber/secret`
	if [ -n "$SECRET" ] ; then
		echo "Updating component authentication secret in ejabberd config file..."
		perl -pi -e "s/>secret</$SECRET/" /etc/jabber/ejabberd.cfg
	fi
fi

if [ ! -f /etc/jabber/cookie ] ; then
        echo "Generating erl authentication cookie..."
        umask 066
        perl -e 'open R,"/dev/urandom"; read R,$r,16;
                printf "%02x",ord(chop $r) while($r);' > /etc/jabber/cookie
fi

/sbin/chkconfig --add ejabberd
if [ -r /var/lock/subsys/ejabberd ]; then
	/etc/rc.d/init.d/ejabberd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/ejabberd start\" to start ejabberd server."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/ejabberd ]; then
		/etc/rc.d/init.d/ejabberd stop >&2
	fi
	/sbin/chkconfig --del ejabberd
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog doc
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/*
%attr(770,root,jabber) /var/log/ejabberd
%{_libdir}/ejabberd
%dir %attr(770,root,jabber) /var/lib/ejabberd
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
