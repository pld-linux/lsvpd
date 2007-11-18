Summary:	VPD/hardware inventory utilities for Linux
Summary(pl.UTF-8):	Narzędzia do inwentaryzacji VPD/sprzętu dla Linuksa
Name:		lsvpd
Version:	1.0.3
Release:	3
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/linux-diag/%{name}-%{version}.tar.gz
# Source0-md5:	5d6cc395deeab1bb926a2f973d4cad1d
Patch0:		%{name}-make.patch
URL:		http://linux-diag.sourceforge.net/Lsvpd.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	db-cxx-devel >= 4.2
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sg3_utils-devel
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(post):	/sbin/ldconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_exec_prefix	/
%define		_libdir		/usr/%{_lib}
%define		_sbindir	/sbin

%description
The lsvpd package contains both the lsvpd, lscfg and lsmcode commands.
These commands, along with a boot-time scanning script called
update-device-tree, constitute a simple hardware inventory system. The
lsvpd command provides Vital Product Data (VPD) about hardware
components to higher-level serviceability tools. The lscfg command
provides a more human-readable format of the VPD, as well as some
system-specific information. lsmcode lists microcode and firmware
levels.

%description -l pl.UTF-8
Pakiet lsvpd zawiera polecenia lsvpd, lscfg i lsmcode. Tworzą one,
wraz z uruchamianym przy starcie systemu skryptem update-device-tree,
prosty system inwentaryzacji sprzętu. Polecenie lsvpd dostarcza VPD
(Vital Product Data) o podzespołach sprzętowych dla narzędzi wyższego
poziomu. Polecenie lscfg dostarcza bardziej czytelną dla człowieka
postać VPD oraz trochę informacji specyficznych dla systemu. lsmcode
wypisuje poziomy mikrokodu i firmware'u.

%package devel
Summary:	Header files for vpd library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki vpd
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for vpd library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki vpd.

%package static
Summary:	Static vpd library
Summary(pl.UTF-8):	Statyczna biblioteka vpd
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static vpd library.

%description static -l pl.UTF-8
Statyczna biblioteka vpd.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make} LIBDB=-ldb_cxx-4.6

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install vpdupdater $RPM_BUILD_ROOT/etc/rc.d/init.d/vpdupdater

install -d $RPM_BUILD_ROOT/%{_lib}
mv -f $RPM_BUILD_ROOT%{_libdir}/libvpd-1.0.so.*.*.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(cd $RPM_BUILD_ROOT/%{_lib}; echo libvpd-1.0.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libvpd-1.0.so

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add vpdupdater

%postun	-p /sbin/ldconfig

%preun
if [ "$1" = "0" ] ; then
	/sbin/chkconfig --del vpdupdater
fi

%triggerpostun -- lsvpd < 1.0.0
/sbin/chkconfig --del lsvpd

%files
%defattr(644,root,root,755)
%doc NEWS README TODO docs/*.html
%attr(755,root,root) /sbin/lscfg
%attr(755,root,root) /sbin/lsmcode
%attr(755,root,root) /sbin/lsvio
%attr(755,root,root) /sbin/lsvpd
%attr(755,root,root) /sbin/vpdupdate
%attr(755,root,root) /%{_lib}/libvpd-1.0.so.*.*.*
%attr(754,root,root) /etc/rc.d/init.d/vpdupdater
%{_mandir}/man8/lscfg.8*
%{_mandir}/man8/lsmcode.8*
%{_mandir}/man8/lsvio.8*
%{_mandir}/man8/lsvpd.8*
%{_mandir}/man8/vpdupdate.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvpd-1.0.so
%{_libdir}/libvpd-1.0.la
%{_includedir}/libvpd-1

%files static
%defattr(644,root,root,755)
%{_libdir}/libvpd-1.0.a
