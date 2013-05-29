%define major	0
%define libname %mklibname mysql-proxy %{major}
%define devname %mklibname mysql-proxy -d

Summary:	A Proxy for the MySQL Client/Server protocol
Name:		mysql-proxy
Version:	0.8.3
Release:	1
License:	GPLv2
Group:		System/Servers
Url:		http://forge.mysql.com/wiki/MySQL_Proxy
Source0:	http://mysql.dataphone.se/Downloads/MySQL-Proxy/mysql-proxy-%{version}.tar.gz
Source1:	http://mysql.dataphone.se/Downloads/MySQL-Proxy/mysql-proxy-%{version}.tar.gz.asc
Source2:	mysql-proxy.init
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	mysql-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(lua)
Requires(preun,post):	rpm-helper

%description
MySQL Proxy is a simple program that sits between your client and MySQL
server(s) that can monitor, analyze or transform their communication. Its
flexibility allows for unlimited uses; common ones include: load balancing;
failover; query analysis; query filtering and modification; and many more.

%package -n	%{libname}
Summary:	Shared libraries for %{name}
Group:		System/Libraries

%description -n	%{libname}
This package contains the shared libraries for %{name}.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C

%description -n	%{devname}
This package contains development files for %{name}.

%prep

%setup -q

cp %{SOURCE2} mysql-proxy.init

%build
%serverbuild

%configure2_5x \
	--with-lua

%make LIBS='-llua'

%install
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}/var/run/%{name}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_includedir}/%{name}

%makeinstall
# bork
mv %{buildroot}%{_bindir}/mysql-proxy %{buildroot}%{_sbindir}/
mv %{buildroot}%{_includedir}/*.h %{buildroot}%{_includedir}/%{name}/

install -m0755 mysql-proxy.init %{buildroot}%{_initrddir}/%{name}
install -m0644 examples/*.lua %{buildroot}%{_datadir}/%{name}/

cat > mysql-proxy.sysconfig << EOF
MYSQL_PROXY_OPTIONS="--daemon --proxy-lua-script %{_datadir}/%{name}/tutorial-basic.lua --plugin-dir=%{_libdir}/mysql-proxy/plugins"
EOF

install -m0644 mysql-proxy.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%doc AUTHORS NEWS README README.TESTS
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/mysql-proxy
%{_bindir}/mysql-binlog-dump
%{_bindir}/mysql-myisam-dump
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.lua
%dir /var/run/%{name}
%dir %{_libdir}/mysql-proxy
%dir %{_libdir}/mysql-proxy/plugins
%dir %{_libdir}/mysql-proxy/lua
%dir %{_libdir}/mysql-proxy/lua/proxy
%{_libdir}/mysql-proxy/plugins/*.so
%{_libdir}/mysql-proxy/lua/*.so
%{_libdir}/mysql-proxy/lua/proxy/*.lua
%{_libdir}/mysql-proxy/lua/*.lua

%files -n %{libname}
%{_libdir}/libmysql-proxy.so.%{major}*
%{_libdir}/libmysql-chassis-glibext.so.%{major}*
%{_libdir}/libmysql-chassis-timing.so.%{major}*
%{_libdir}/libmysql-chassis.so.%{major}*

%files -n %{devname}
%doc COPYING
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/mysql-chassis.pc
%{_libdir}/pkgconfig/mysql-proxy.pc

