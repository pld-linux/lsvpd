#
# Conditional build:
%bcond_with	rtas	# RTAS support (PowerPC)
#
%ifarch ppc ppc64
%define	with_rtas	1
%endif
Summary:	VPD/hardware inventory utilities for Linux
Summary(pl.UTF-8):	Narzędzia do inwentaryzacji VPD/sprzętu dla Linuksa
Name:		lsvpd
Version:	1.7.0
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/linux-diag/%{name}-%{version}.tar.gz
# Source0-md5:	f412a63741dc29e6a23999793237b524
Source1:	vpdupdater.init
Source2:	vpdupdater.sysconfig
Patch0:		%{name}-make.patch
Patch1:		%{name}-nortas.patch
URL:		http://linux-diag.sourceforge.net/Lsvpd.html
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_rtas:BuildRequires:	librtas-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.0
BuildRequires:	libvpd-cxx-devel >= 2
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sg3_utils-devel
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(post):	/sbin/ldconfig
Requires:	/lib/hwdata/pci.ids
Requires:	/lib/hwdata/usb.ids
Requires:	hwdata >= 0.243-5
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_rtas:ac_cv_lib_rtas_rtas_get_vpd=no}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/vpdupdater
install -D -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/vpdupdater

%clean
rm -rf $RPM_BUILD_ROOT

%post
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
%doc AUTHORS NEWS README TODO docs/*.html
%attr(755,root,root) %{_sbindir}/invscout
%attr(755,root,root) %{_sbindir}/lscfg
%attr(755,root,root) %{_sbindir}/lsmcode
%attr(755,root,root) %{_sbindir}/lsvio
%attr(755,root,root) %{_sbindir}/lsvpd
%attr(755,root,root) %{_sbindir}/vpdupdate
%dir %{_sysconfdir}/lsvpd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lsvpd/cpu_mod_conv.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lsvpd/scsi_templates.conf
%attr(754,root,root) /etc/rc.d/init.d/vpdupdater
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/vpdupdater
%{_mandir}/man8/lscfg.8*
%{_mandir}/man8/lsmcode.8*
%{_mandir}/man8/lsvio.8*
%{_mandir}/man8/lsvpd.8*
%{_mandir}/man8/vpdupdate.8*
