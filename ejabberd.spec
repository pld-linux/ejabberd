Summary:	Fault-tolerant distributed Jabber/XMPP server
Summary(pl):	Odporny na awarie rozproszony serwer Jabbera/XMPP
Name:		ejabberd
Version:	0.7.5
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	http://www.jabberstudio.org/files/ejabberd/%{name}-%{version}.tar.gz
# Source0-md5:	c9f900ed535cb446e8b567048514c705
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.sh
Source4:	%{name}ctl.sh
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-64bit_fix.patch
URL:		http://ejabberd.jabberstudio.org/
BuildRequires:	autoconf
BuildRequires:	erlang >= R8B
BuildRequires:	expat >= 1.95
PreReq:		rc-scripts
Requires(post): jabber-common
Requires(post):	textutils
Requires(post):	/usr/bin/perl
Requires(post,preun):	/sbin/chkconfig
Requires:	erlang
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ejabberd is a Free and Open Source fault-tolerant distributed Jabber
server. It is written mostly in Erlang.

%description -l pl
ejabberd to darmowy, z otwartymi ¼ród³ami, odporny na awarie
rozproszony serwer Jabbera. Jest napisany w wiêkszo¶ci w Erlangu.

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

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install %{SOURCE3} $RPM_BUILD_ROOT/%{_sbindir}/%{name}
install %{SOURCE4} $RPM_BUILD_ROOT/%{_sbindir}/%{name}ctl

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
%attr(640,root,jabber) %config(noreplace) %verify(not md5 size mtime) /etc/jabber/*
%attr(770,root,jabber) /var/log/ejabberd
%{_libdir}/ejabberd
%dir %attr(770,root,jabber) /var/lib/ejabberd
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/%{name}
