Summary:	A Proxy for the MySQL Client/Server protocol
Name:		mysql-proxy
Version:	0.6.0
Release:	%mkrel 1
License:	GPL
Group:		System/Servers
URL:		http://forge.mysql.com/wiki/MySQL_Proxy
Source0:	http://mysql.dataphone.se/Downloads/MySQL-Proxy/mysql-proxy-0.6.0.tar.gz
Source1:	http://mysql.dataphone.se/Downloads/MySQL-Proxy/mysql-proxy-0.6.0.tar.gz.asc
Source2:	mysql-proxy.init
Requires(preun): rpm-helper
Requires(post): rpm-helper
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	glib2-devel
BuildRequires:	libevent-devel
BuildRequires:	lua-devel >= 5.1
BuildRequires:	mysql-devel
BuildRequires:	pkgconfig
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
MySQL Proxy is a simple program that sits between your client and MySQL
server(s) that can monitor, analyze or transform their communication. Its
flexibility allows for unlimited uses; common ones include: load balancing;
failover; query analysis; query filtering and modification; and many more.

%prep

%setup -q

cp %{SOURCE2} mysql-proxy.init


%build
%serverbuild

%configure2_5x \
    --with-lua

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}/var/run/%{name}

%makeinstall

install -m0755 mysql-proxy.init %{buildroot}%{_initrddir}/%{name}
install -m0644 examples/*.lua %{buildroot}%{_datadir}/%{name}/

cat > mysql-proxy.sysconfig << EOF
MYSQL_PROXY_OPTIONS="--daemon --proxy-lua-script %{_datadir}/%{name}/tutorial-basic.lua"
EOF

install -m0644 mysql-proxy.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# cleanup
rm -f %{buildroot}%{_datadir}/*.lua

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README README.TESTS
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0755,root,root) %{_sbindir}/%{name}
%{_datadir}/%{name}
%dir /var/run/%{name}

