Summary:	VPD/hardware inventory utilities for Linux
Summary(pl):	Narz�dzia do inwentaryzacji VPD/sprz�tu dla Linuksa
Name:		lsvpd
Version:	0.13.0
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/linux-diag/%{name}-%{version}.tar.gz
# Source0-md5:	189068fe7e7ce78de9322bbdebb64fd9
URL:		http://linux-diag.sourceforge.net/Lsvpd.html
BuildRequires:	perl-base
BuildRequires:	sed >= 4.0
BuildRequires:	sg3_utils-devel >= 1.01
BuildRequires:	sysfsutils-devel
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	/bin/bash
Requires:	/bin/sed
Requires:	/bin/sh
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
Pakiet lsvpd zawiera polecenia lsvpd, lscfg i lsmcode. Tworz� one,
wraz z uruchamianym przy starcie systemu skryptem update-device-tree,
prosty system inwentaryzacji sprz�tu. Polecenie lsvpd dostarcza VPD
(Vital Product Data) o podzespo�ach sprz�towych dla narz�dzi wy�szego
poziomu. Polecenie lscfg dostarcza bardziej czyteln� dla cz�owieka
posta� VPD oraz troch� informacji specyficznych dla systemu. lsmcode
wypisuje poziomy mikrokodu i firmware'u.

%prep
%setup -q

sed -i -e "s,#!/bin/sh,#!/bin/bash," scripts/lsvpd.in
sed -i -e 's,sysfs/,,' src/device_sysfs.c src/sysfs.c

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -I../lib" \
	LDLIBS="-lsysfs -lsgutils"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install debian/init.d $RPM_BUILD_ROOT/etc/rc.d/init.d/lsvpd
# don't install this right now.  It can crash systems.
rm -f $RPM_BUILD_ROOT/lib/lsvpd/pci_vpd_rom_grab

install -d $RPM_BUILD_ROOT/etc/cron.daily
install scripts/lsvpd.cron.daily $RPM_BUILD_ROOT/etc/cron.daily/lsvpd

ln -sf /usr/bin/find $RPM_BUILD_ROOT/lib/lsvpd/find

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add lsvpd

%preun
if [ "$1" = "0" ] ; then
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
/lib/lsvpd/scsihost.conf
/lib/lsvpd/scsivpd.conf
%attr(755,root,root) /lib/lsvpd/device_handler
%attr(755,root,root) /lib/lsvpd/ibm_vpd_render
%attr(755,root,root) /lib/lsvpd/lsvpd_test
%attr(755,root,root) /lib/lsvpd/pci_ethernet_map
%attr(755,root,root) /lib/lsvpd/pci_lookup
%attr(755,root,root) /lib/lsvpd/pci_scsi_map
%attr(755,root,root) /lib/lsvpd/pci_vpd_cap_grab
%attr(755,root,root) /lib/lsvpd/tdump
%attr(755,root,root) /lib/lsvpd/tidy_lsvpd_dbs
%attr(755,root,root) /lib/lsvpd/tidy_subdirs
%attr(755,root,root) /lib/lsvpd/update-vpd.hotplug
%attr(755,root,root) /lib/lsvpd/vpd-name-crosslink.hotplug
%attr(754,root,root) /etc/rc.d/init.d/lsvpd
%attr(755,root,root) /etc/cron.daily/lsvpd
%{_mandir}/man8/*
