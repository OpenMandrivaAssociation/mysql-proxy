%define major 0
%define libname %mklibname mysql-proxy %{major}
%define libchassis %mklibname mysql-chassis %{major}
%define libchassis_glibext %mklibname mysql-chassis-glibext %{major}
%define libchassis_timing %mklibname mysql-chassis-timing %{major}
%define devname %mklibname mysql-proxy -d

Summary:	A Proxy for the MySQL Client/Server protocol
Name:		mysql-proxy
Version:	0.8.4
Release:	2
License:	GPLv2+
Group:		System/Servers
Url:		http://forge.mysql.com/wiki/MySQL_Proxy
Source0:	http://mysql.dataphone.se/Downloads/MySQL-Proxy/mysql-proxy-%{version}.tar.gz
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

%post
%_post_service %{name}

%preun
%_preun_service %{name}

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
This package contains shared library for %{name}.

%files -n %{libname}
%{_libdir}/libmysql-proxy.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libchassis}
Summary:	Shared library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}mysql-proxy0 < 0.8.4

%description -n %{libchassis}
This package contains shared library for %{name}.

%files -n %{libchassis}
%{_libdir}/libmysql-chassis.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libchassis_glibext}
Summary:	Shared library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}mysql-proxy0 < 0.8.4

%description -n %{libchassis_glibext}
This package contains shared library for %{name}.

%files -n %{libchassis_glibext}
%{_libdir}/libmysql-chassis-glibext.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libchassis_timing}
Summary:	Shared library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}mysql-proxy0 < 0.8.4

%description -n %{libchassis_timing}
This package contains shared library for %{name}.

%files -n %{libchassis_timing}
%{_libdir}/libmysql-chassis-timing.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libchassis} = %{EVRD}
Requires:	%{libchassis_glibext} = %{EVRD}
Requires:	%{libchassis_timing} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
This package contains development files for %{name}.

%files -n %{devname}
%doc COPYING
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/mysql-chassis.pc
%{_libdir}/pkgconfig/mysql-proxy.pc

#----------------------------------------------------------------------------

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

