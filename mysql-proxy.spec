%define major 0
%define libname %mklibname mysql-proxy %{major}
%define develname %mklibname mysql-proxy -d

Summary:	A Proxy for the MySQL Client/Server protocol
Name:		mysql-proxy
Version:	0.8.1
Release:	%mkrel 1
License:	GPL
Group:		System/Servers
URL:		http://forge.mysql.com/wiki/MySQL_Proxy
Source0:	http://mysql.dataphone.se/Downloads/MySQL-Proxy/mysql-proxy-%{version}.tar.gz
Source1:	http://mysql.dataphone.se/Downloads/MySQL-Proxy/mysql-proxy-%{version}.tar.gz.asc
Source2:	mysql-proxy.init
Requires(preun): rpm-helper
Requires(post): rpm-helper
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	glib2-devel
BuildRequires:	libevent-devel >= 1.4
BuildRequires:	lua-devel >= 5.1
BuildRequires:	mysql-devel
BuildRequires:	pkgconfig
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/C

%description -n	%{develname}
This package contains development files for %{name}.

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

# cleanup
find %{buildroot}%{_libdir} -name "*.la" | xargs rm -f

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
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
%defattr(-,root,root)
%doc COPYING
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/mysql-chassis.pc
%{_libdir}/pkgconfig/mysql-proxy.pc
