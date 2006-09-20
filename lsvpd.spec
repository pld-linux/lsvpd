Summary:	VPD/hardware inventory utilities for Linux
Summary(pl):	Narzêdzia do inwentaryzacji VPD/sprzêtu dla Linuksa
Name:		lsvpd
Version:	0.16.0
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/linux-diag/%{name}-%{version}.tar.gz
# Source0-md5:	d3abbecb7056816fe3f6ce6729b433cc
URL:		http://linux-diag.sourceforge.net/Lsvpd.html
BuildRequires:	gcc >= 4.0.0
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	sg3_utils-devel >= 1.01
Requires(post,preun):	/sbin/chkconfig
Requires:	/bin/bash
Requires:	/bin/sed
Requires:	/bin/sh
Requires:	rc-scripts
Requires:	sg3_utils >= 1.01
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

%description -l pl
Pakiet lsvpd zawiera polecenia lsvpd, lscfg i lsmcode. Tworz± one,
wraz z uruchamianym przy starcie systemu skryptem update-device-tree,
prosty system inwentaryzacji sprzêtu. Polecenie lsvpd dostarcza VPD
(Vital Product Data) o podzespo³ach sprzêtowych dla narzêdzi wy¿szego
poziomu. Polecenie lscfg dostarcza bardziej czyteln± dla cz³owieka
postaæ VPD oraz trochê informacji specyficznych dla systemu. lsmcode
wypisuje poziomy mikrokodu i firmware'u.

%prep
%setup -q
sed -i -e "s,#!/bin/sh,#!/bin/bash," scripts/lsvpd.in

%build
# disable unit-at-a-time - see src/init.h
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fno-unit-at-a-time -Wall -Werror -I../lib" \
	LDLIBS="-lsgutils"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install debian/init.d $RPM_BUILD_ROOT/etc/rc.d/init.d/lsvpd
# don't install this right now.  It can crash systems.
#rm -f $RPM_BUILD_ROOT/lib/lsvpd/pci_vpd_rom_grab

install -d $RPM_BUILD_ROOT/etc/cron.daily
install debian/cron.daily $RPM_BUILD_ROOT/etc/cron.daily/lsvpd

ln -sf /usr/bin/find $RPM_BUILD_ROOT/lib/lsvpd/find

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add lsvpd
%service lsvpd restart

%preun
if [ "$1" = "0" ] ; then
	%service lsvpd stop
	/sbin/chkconfig --del lsvpd
fi

%files
%defattr(644,root,root,755)
%doc NEWS README TODO docs/*.html
%attr(755,root,root) /sbin/lsvpd
%attr(755,root,root) /sbin/lscfg
%attr(755,root,root) /sbin/lsmcode
%attr(755,root,root) /sbin/lsvio
%attr(755,root,root) /sbin/update-lsvpd-db
%dir /lib/lsvpd
/lib/lsvpd/common.d
/lib/lsvpd/common-post.d
/lib/lsvpd/debug.bash
/lib/lsvpd/ide_mf.map
/lib/lsvpd/lscfg.d
/lib/lsvpd/lsmcode.d
/lib/lsvpd/lsvio.d
/lib/lsvpd/lsvpd-functions.bash
/lib/lsvpd/lsvpd.d
/lib/lsvpd/pci.ids
/lib/lsvpd/query.d
/lib/lsvpd/scan.d
/lib/lsvpd/scsivpd.conf
%attr(755,root,root) /lib/lsvpd/adapter_pci_legacy
%attr(755,root,root) /lib/lsvpd/ibm_vpd_render
%attr(755,root,root) /lib/lsvpd/node_handler
%attr(755,root,root) /lib/lsvpd/tdump
%attr(754,root,root) /etc/rc.d/init.d/lsvpd
%attr(755,root,root) /etc/cron.daily/lsvpd
%{_mandir}/man8/*
