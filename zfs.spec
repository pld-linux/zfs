# TODO:
# - PLDify init script
#
# Conditional build:
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_without	python2		# CPython 2.x module
%bcond_without	python3		# CPython 3.x module
%bcond_with	verbose		# verbose build (V=1)
#
# The goal here is to have main, userspace, package built once with
# simple release number, and only rebuild kernel packages with kernel
# version as part of release number, without the need to bump release
# with every kernel change.
%if 0%{?_pld_builder:1} && %{with kernel} && %{with userspace}
%{error:kernel and userspace cannot be built at the same time on PLD builders}
exit 1
%endif

%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%define		_duplicate_files_terminate_build	0

#define	pre	rc3
%define	rel	0.1
%define	pname	zfs
Summary:	Native Linux port of the ZFS filesystem
Summary(pl.UTF-8):	Natywny linuksowy port systemu plików ZFS
Name:		%{pname}%{?_pld_builder:%{?with_kernel:-kernel}}%{_alt_kernel}
Version:	2.2.0
Release:	%{rel}%{?_pld_builder:%{?with_kernel:@%{_kernel_ver_str}}}
License:	CDDL
Group:		Applications/System
Source0:	https://github.com/openzfs/zfs/releases/download/zfs-%{version}/%{pname}-%{version}.tar.gz
# Source0-md5:	d7e2ec4c52d6a48653ce4a5b96c24a01
Patch0:		initdir.patch
URL:		https://zfsonlinux.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with kernel}
%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2}
%endif
%if %{with userspace}
# only for mmap_libaio test command
#BuildRequires:	libaio-devel
BuildRequires:	libblkid-devel
BuildRequires:	libselinux-devel
BuildRequires:	libtirpc-devel
BuildRequires:	libuuid-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	udev-devel
BuildRequires:	zlib-devel
%if %{with python2}
BuildRequires:	python-cffi
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-cffi
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%endif
%if %{with python2} || %{with python3}
BuildRequires:	rpm-pythonprov
%endif
%endif
Requires:	%{pname}-libs = %{version}-%{release}
Obsoletes:	spl < 0.7.9-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dracutlibdir	%{_prefix}/lib/dracut

%description
ZFS is an advanced file system and volume manager which was originally
developed for Solaris and is now maintained by the Illumos community.

ZFS on Linux, which is also known as ZoL, is currently feature
complete. It includes fully functional and stable SPA, DMU, ZVOL, and
ZPL layers.

%description -l pl.UTF-8
ZFS to zaawansowany system plików i zarządca wolumenów, oryginalnie
stworzony dla Solarisa, obecnie utrzymywany przez społeczność Illumos.

ZFS dla Linuksa, znany takża jako ZoL (ZFS on Linux), jest obecnie w
pełni funkcjonalny. Zawiera w pełni funkcjonalne i stabilne warstwy
SPA, DMU, ZVOL i ZPL.

%package libs
Summary:	ZFS on Linux libraries
Summary(pl.UTF-8):	Biblioteki ZFS-a dla Linuksa
License:	CDDL
Group:		Libraries
Requires(post,postun):	/sbin/ldconfig

%description libs
ZFS on Linux libraries.

%description libs -l pl.UTF-8
Biblioteki ZFS-a dla Linuksa.

%package devel
Summary:	Header files for ZFS libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek ZFS-a
License:	CDDL
Group:		Development/Libraries
Requires:	%{pname}-libs = %{version}-%{release}
Requires:	libselinux-devel
Requires:	libtirpc-devel
Requires:	libuuid-devel
Requires:	zlib-devel

%description devel
Header files for ZFS libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek ZFS-a.

%package static
Summary:	Static ZFS libraries
Summary(pl.UTF-8):	Statyczne biblioteki ZFS-a
License:	CDDL
Group:		Development/Libraries
Requires:	%{pname}-devel = %{version}-%{release}

%description static
Static ZFS libraries.

%description static -l pl.UTF-8
Statyczne biblioteki ZFS-a.

%package -n dracut-zfs
Summary:	ZFS support for Dracut
Summary(pl.UTF-8):	Obsługa ZFS-a dla Dracuta
Group:		Applications/System
Requires:	%{pname} = %{version}-%{release}
Requires:	dracut

%description -n dracut-zfs
ZFS support for Dracut.

%description -n dracut-zfs -l pl.UTF-8
Obsługa ZFS-a dla Dracuta.

%package -n pam-pam_zfs_key
Summary:	PAM module to unlock ZFS datasets for user
Summary(pl.UTF-8):	Moduł PAM do odblokowywania zbiorów danych ZFS dla użytkownika
Group:		Libraries
Requires:	%{pname}-libs = %{version}-%{release}
Requires:	pam

%description -n pam-pam_zfs_key
PAM module to unlock ZFS datasets for user.

%description -n pam-pam_zfs_key -l pl.UTF-8
Moduł PAM do odblokowywania zbiorów danych ZFS dla użytkownika.

%package -n python-pyzfs
Summary:	Python 2 wrapper for libzfs_core C library
Summary(pl.UTF-8):	Interfejs Pythona 2 do biblioteki C libzfs_core
License:	Apache v2.0
Group:		Libraries/Python
Requires:	%{pname}-libs = %{version}-%{release}

%description -n python-pyzfs
Python 2 wrapper for libzfs_core C library.

%description -n python-pyzfs -l pl.UTF-8
Interfejs Pythona 2 do biblioteki C libzfs_core.

%package -n python3-pyzfs
Summary:	Python 3 wrapper for libzfs_core C library
Summary(pl.UTF-8):	Interfejs Pythona 3 do biblioteki C libzfs_core
License:	Apache v2.0
Group:		Libraries/Python
Requires:	%{pname}-libs = %{version}-%{release}

%description -n python3-pyzfs
Python 3 wrapper for libzfs_core C library.

%description -n python3-pyzfs -l pl.UTF-8
Interfejs Pythona 3 do biblioteki C libzfs_core.

%package -n kernel-zfs-common-devel
Summary:	ZFS Linux kernel headers
Summary(pl.UTF-8):	ZFS - pliki nagłówkowe jądra Linuksa
Group:		Development/Building
Obsoletes:	kernel-spl-common-devel < 0.7.9-2

%description -n kernel-zfs-common-devel
ZFS Linux kernel headers common for all PLD kernel versions.

%description -n kernel-zfs-common-devel -l pl.UTF-8
ZFS - pliki nagłówkowe jądra Linuksa wspólne na wszystkich
wersji jąder PLD.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-zfs\
Summary:	ZFS Linux kernel modules\
Summary(pl.UTF-8):	ZFS - moduły jądra Linuksa\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
\
%description -n kernel%{_alt_kernel}-zfs\
ZFS Linux kernel modules.\
\
%description -n kernel%{_alt_kernel}-zfs -l pl.UTF-8\
ZFS - moduły jądra Linuksa.\
\
%package -n kernel%{_alt_kernel}-zfs-devel\
Summary:	ZFS Linux kernel headers\
Summary(pl.UTF-8):	ZFS - pliki nagłówkowe jądra Linuksa\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Development/Building\
Requires:	kernel%{_alt_kernel}-headers\
Requires:	kernel-zfs-common-devel\
Obsoletes:	kernel-spl-devel < 0.7.9-2\
\
%description -n kernel%{_alt_kernel}-zfs-devel\
ZFS Linux kernel headers configured for PLD kernel%{_alt_kernel},\
version %{_kernel_ver}.\
\
%description -n kernel%{_alt_kernel}-zfs-devel -l pl.UTF-8\
ZFS - pliki nagłówkowe jądra Linuksa skonfigurowane dla jądra PLD z\
pakietu kernel%{_alt_kernel} w wersji %{_kernel_ver}.\
\
%files -n kernel%{_alt_kernel}-zfs\
%defattr(644,root,root,755)\
/lib/modules/%{_kernel_ver}/misc/spl.ko*\
/lib/modules/%{_kernel_ver}/misc/zfs.ko*\
\
%files -n kernel%{_alt_kernel}-zfs-devel\
%defattr(644,root,root,755)\
/usr/src/zfs-%{version}/%{_kernel_ver}\
\
%post	-n kernel%{_alt_kernel}-zfs\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-zfs\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
%configure \\\
	--disable-silent-rules \\\
	--with-config="kernel" \\\
	--with-linux=%{_kernelsrcdir}\\\
	--with-linux-obj=%{_kernelsrcdir}\
\
%{__make} clean\
%{__make} %{?with_verbose:V=1}\
p=`pwd`\
%{__make} install DESTDIR=$p/installed INSTALL_MOD_DIR=misc\
%{nil}

%{?with_kernel:%{expand:%create_kernel_packages}}

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
      cmd/arc_summary

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+@PYTHON_SHEBANG@(\s|$),#!%{__python3}\1,' \
      cmd/arcstat.in \
      cmd/dbufstat.in \
      cmd/zilstat.in

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+bash(\s|$),#!/bin/bash\1,' \
      contrib/dracut/02zfsexpandknowledge/module-setup.sh.in \
      contrib/dracut/90zfs/module-setup.sh.in \
      scripts/zimport.sh \
      scripts/zloop.sh

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%{?with_kernel:%{expand:%build_kernel_packages}}

%if %{with userspace}
%configure \
	--disable-silent-rules \
	--enable-pam \
	--enable-systemd \
	--with-config="user" \
	--with-linux=%{_kernelsrcdir} \
	--with-pammoduledir=/%{_lib}/security \
	--with-systemdunitdir=%{systemdunitdir} \
	--with-systemdpresetdir=/etc/systemd/system-preset \
	--with-systemdmodulesloaddir=/etc/modules-load.d \
	--with-systemdgeneratordir=/lib/systemd/system-generators \
	--with-udevdir=/lib/udev

%{__make} \
	%{?with_verbose:V=1}

%if %{with python2}
cd contrib/pyzfs
%py_build
cd ../..
%endif

%if %{with python3}
cd contrib/pyzfs
%py3_build
cd ../..
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
install -d $RPM_BUILD_ROOT
cp -a installed/* $RPM_BUILD_ROOT
%endif

%if %{with userspace}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	DEFAULT_INIT_DIR=/etc/rc.d/init.d

%if %{with python2}
%{__rm} -rf $RPM_BUILD_ROOT%{py_sitescriptdir}
cd contrib/pyzfs
%py_install

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}

%py_postclean
cd ../..
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/libzfs_core/test
%endif

%if %{with python3}
cd contrib/pyzfs
%py3_install
cd ../..
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/libzfs_core/test
%endif

# Debian specific stuff
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/initramfs-tools

%{__rm} $RPM_BUILD_ROOT/%{_lib}/security/pam_zfs_key.la
# Ubuntu PAM config framework file
%{__rm} $RPM_BUILD_ROOT%{_datadir}/pam-configs/zfs_key

# Package these? These are integration tests of the implementation.
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/zfs/{zfs-tests,test-runner,runfiles}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/{raidz_test,test-runner}.1*
%{__rm} $RPM_BUILD_ROOT%{_bindir}/raidz_test
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc AUTHORS COPYRIGHT LICENSE NEWS NOTICE README.md
%attr(755,root,root) /sbin/mount.zfs
%attr(755,root,root) %{_bindir}/arc_summary
%attr(755,root,root) %{_bindir}/arcstat
%attr(755,root,root) %{_bindir}/dbufstat
%attr(755,root,root) %{_bindir}/zilstat
%attr(755,root,root) %{_bindir}/zvol_wait
%attr(755,root,root) %{_sbindir}/fsck.zfs
%attr(755,root,root) %{_sbindir}/zdb
%attr(755,root,root) %{_sbindir}/zed
%attr(755,root,root) %{_sbindir}/zfs
%attr(755,root,root) %{_sbindir}/zfs_ids_to_path
%attr(755,root,root) %{_sbindir}/zgenhostid
%attr(755,root,root) %{_sbindir}/zhack
%attr(755,root,root) %{_sbindir}/zinject
%attr(755,root,root) %{_sbindir}/zpool
%attr(755,root,root) %{_sbindir}/zstream
%attr(755,root,root) %{_sbindir}/zstreamdump
%attr(755,root,root) %{_sbindir}/ztest
%dir %{_sysconfdir}/zfs
# package *.example as %doc? (they cannot act as default configuration)
%{_sysconfdir}/zfs/vdev_id.conf.*.example
%dir %{_sysconfdir}/zfs/zed.d
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zfs/zed.d/*.sh
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zfs/zed.d/zed.rc
%dir %{_sysconfdir}/zfs/zpool.d
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zfs/zpool.d/*
%attr(754,root,root) /etc/rc.d/init.d/zfs-import
%attr(754,root,root) /etc/rc.d/init.d/zfs-mount
%attr(754,root,root) /etc/rc.d/init.d/zfs-share
%attr(754,root,root) /etc/rc.d/init.d/zfs-zed
%attr(754,root,root) /etc/rc.d/init.d/zfs-load-key
%config(noreplace) %verify(not md5 mtime size) /etc/default/zfs
/etc/zfs/zfs-functions
%config(noreplace) %verify(not md5 mtime size) /etc/modules-load.d/zfs.conf
# for zpool iostat/status -c smart
#/ets/sudoers.d/zfs
/etc/systemd/system-preset/50-zfs.preset
/lib/systemd/system-generators/zfs-mount-generator
%{systemdunitdir}/zfs.target
%{systemdunitdir}/zfs-import.service
%{systemdunitdir}/zfs-import.target
%{systemdunitdir}/zfs-import-cache.service
%{systemdunitdir}/zfs-import-scan.service
%{systemdunitdir}/zfs-load-key.service
%{systemdunitdir}/zfs-mount.service
%{systemdunitdir}/zfs-scrub@.service
%{systemdunitdir}/zfs-scrub-monthly@.timer
%{systemdunitdir}/zfs-scrub-weekly@.timer
%{systemdunitdir}/zfs-share.service
%{systemdunitdir}/zfs-trim-monthly@.timer
%{systemdunitdir}/zfs-trim-weekly@.timer
%{systemdunitdir}/zfs-trim@.service
%{systemdunitdir}/zfs-volume-wait.service
%{systemdunitdir}/zfs-volumes.target
%{systemdunitdir}/zfs-zed.service
%attr(755,root,root) /lib/udev/vdev_id
%attr(755,root,root) /lib/udev/zvol_id
/lib/udev/rules.d/60-zvol.rules
/lib/udev/rules.d/69-vdev.rules
/lib/udev/rules.d/90-zfs.rules
%dir %{_libexecdir}/zfs
%dir %{_libexecdir}/zfs/zed.d
%attr(755,root,root) %{_libexecdir}/zfs/zed.d/*.sh
%dir %{_libexecdir}/zfs/zpool.d
%attr(755,root,root) %{_libexecdir}/zfs/zpool.d/*
%dir %{_datadir}/zfs
%attr(755,root,root) %{_datadir}/zfs/*.sh
%attr(755,root,root) %{_libexecdir}/zfs/zpool_influxdb
%{_datadir}/zfs/compatibility.d
%{_mandir}/man1/arcstat.1*
%{_mandir}/man1/zhack.1*
%{_mandir}/man1/ztest.1*
%{_mandir}/man1/zvol_wait.1*
%{_mandir}/man4/spl.4*
%{_mandir}/man4/zfs.4*
%{_mandir}/man5/vdev_id.conf.5*
%{_mandir}/man7/vdevprops.7*
%{_mandir}/man7/zfsconcepts.7*
%{_mandir}/man7/zfsprops.7*
%{_mandir}/man7/zpool-features.7*
%{_mandir}/man7/zpoolconcepts.7*
%{_mandir}/man7/zpoolprops.7*
%{_mandir}/man8/fsck.zfs.8*
%{_mandir}/man8/mount.zfs.8*
%{_mandir}/man8/vdev_id.8*
%{_mandir}/man8/zdb.8*
%{_mandir}/man8/zed.8*
%{_mandir}/man8/zfs.8*
%{_mandir}/man8/zfs-allow.8*
%{_mandir}/man8/zfs-bookmark.8*
%{_mandir}/man8/zfs-change-key.8*
%{_mandir}/man8/zfs-clone.8*
%{_mandir}/man8/zfs-create.8*
%{_mandir}/man8/zfs-destroy.8*
%{_mandir}/man8/zfs-diff.8*
%{_mandir}/man8/zfs-get.8*
%{_mandir}/man8/zfs-groupspace.8*
%{_mandir}/man8/zfs-hold.8*
%{_mandir}/man8/zfs-inherit.8*
%{_mandir}/man8/zfs-jail.8*
%{_mandir}/man8/zfs-list.8*
%{_mandir}/man8/zfs-load-key.8*
%{_mandir}/man8/zfs-mount.8*
%{_mandir}/man8/zfs-mount-generator.8*
%{_mandir}/man8/zfs-program.8*
%{_mandir}/man8/zfs-project.8*
%{_mandir}/man8/zfs-projectspace.8*
%{_mandir}/man8/zfs-promote.8*
%{_mandir}/man8/zfs-receive.8*
%{_mandir}/man8/zfs-recv.8*
%{_mandir}/man8/zfs-redact.8*
%{_mandir}/man8/zfs-release.8*
%{_mandir}/man8/zfs-rename.8*
%{_mandir}/man8/zfs-rollback.8*
%{_mandir}/man8/zfs-send.8*
%{_mandir}/man8/zfs-set.8*
%{_mandir}/man8/zfs-share.8*
%{_mandir}/man8/zfs-snapshot.8*
%{_mandir}/man8/zfs-unallow.8*
%{_mandir}/man8/zfs-unjail.8*
%{_mandir}/man8/zfs-unload-key.8*
%{_mandir}/man8/zfs-unzone.8*
%{_mandir}/man8/zfs-unmount.8*
%{_mandir}/man8/zfs-upgrade.8*
%{_mandir}/man8/zfs-userspace.8*
%{_mandir}/man8/zfs-wait.8*
%{_mandir}/man8/zfs-zone.8*
%{_mandir}/man8/zfs_ids_to_path.8*
%{_mandir}/man8/zgenhostid.8*
%{_mandir}/man8/zinject.8*
%{_mandir}/man8/zpool.8*
%{_mandir}/man8/zpool-add.8*
%{_mandir}/man8/zpool-attach.8*
%{_mandir}/man8/zpool-checkpoint.8*
%{_mandir}/man8/zpool-clear.8*
%{_mandir}/man8/zpool-create.8*
%{_mandir}/man8/zpool-destroy.8*
%{_mandir}/man8/zpool-detach.8*
%{_mandir}/man8/zpool-events.8*
%{_mandir}/man8/zpool-export.8*
%{_mandir}/man8/zpool-get.8*
%{_mandir}/man8/zpool-history.8*
%{_mandir}/man8/zpool-import.8*
%{_mandir}/man8/zpool-initialize.8*
%{_mandir}/man8/zpool-iostat.8*
%{_mandir}/man8/zpool-labelclear.8*
%{_mandir}/man8/zpool-list.8*
%{_mandir}/man8/zpool-offline.8*
%{_mandir}/man8/zpool-online.8*
%{_mandir}/man8/zpool-reguid.8*
%{_mandir}/man8/zpool-remove.8*
%{_mandir}/man8/zpool-reopen.8*
%{_mandir}/man8/zpool-replace.8*
%{_mandir}/man8/zpool-resilver.8*
%{_mandir}/man8/zpool-scrub.8*
%{_mandir}/man8/zpool-set.8*
%{_mandir}/man8/zpool-split.8*
%{_mandir}/man8/zpool-status.8*
%{_mandir}/man8/zpool-sync.8*
%{_mandir}/man8/zpool-trim.8*
%{_mandir}/man8/zpool-upgrade.8*
%{_mandir}/man8/zpool-wait.8*
%{_mandir}/man8/zpool_influxdb.8*
%{_mandir}/man8/zstream.8*
%{_mandir}/man8/zstreamdump.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnvpair.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnvpair.so.3
%attr(755,root,root) %{_libdir}/libuutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libuutil.so.3
%attr(755,root,root) %{_libdir}/libzfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzfs.so.4
%attr(755,root,root) %{_libdir}/libzfs_core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzfs_core.so.3
%attr(755,root,root) %{_libdir}/libzfsbootenv.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzfsbootenv.so.1
%attr(755,root,root) %{_libdir}/libzpool.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzpool.so.5

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnvpair.so
%attr(755,root,root) %{_libdir}/libuutil.so
%attr(755,root,root) %{_libdir}/libzfs.so
%attr(755,root,root) %{_libdir}/libzfs_core.so
%attr(755,root,root) %{_libdir}/libzfsbootenv.so
%attr(755,root,root) %{_libdir}/libzpool.so
%{_libdir}/libnvpair.la
%{_libdir}/libuutil.la
%{_libdir}/libzfs.la
%{_libdir}/libzfs_core.la
%{_libdir}/libzfsbootenv.la
%{_libdir}/libzpool.la
%{_includedir}/libspl
%{_includedir}/libzfs
%{_pkgconfigdir}/libzfs.pc
%{_pkgconfigdir}/libzfs_core.pc
%{_pkgconfigdir}/libzfsbootenv.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libnvpair.a
%{_libdir}/libuutil.a
%{_libdir}/libzfs.a
%{_libdir}/libzfs_core.a
%{_libdir}/libzfsbootenv.a
%{_libdir}/libzpool.a

%files -n dracut-zfs
%defattr(644,root,root,755)
%doc contrib/dracut/README.md
%dir %{dracutlibdir}/modules.d/02zfsexpandknowledge
%attr(755,root,root) %{dracutlibdir}/modules.d/02zfsexpandknowledge/module-setup.sh
%dir %{dracutlibdir}/modules.d/90zfs
%attr(755,root,root) %{dracutlibdir}/modules.d/90zfs/export-zfs.sh
%attr(755,root,root) %{dracutlibdir}/modules.d/90zfs/import-opts-generator.sh
%attr(755,root,root) %{dracutlibdir}/modules.d/90zfs/module-setup.sh
%attr(755,root,root) %{dracutlibdir}/modules.d/90zfs/mount-zfs.sh
%attr(755,root,root) %{dracutlibdir}/modules.d/90zfs/parse-zfs.sh
%attr(755,root,root) %{dracutlibdir}/modules.d/90zfs/zfs-env-bootfs.service
%attr(755,root,root) %{dracutlibdir}/modules.d/90zfs/zfs-generator.sh
%attr(755,root,root) %{dracutlibdir}/modules.d/90zfs/zfs-lib.sh
%attr(755,root,root) %{dracutlibdir}/modules.d/90zfs/zfs-load-key.sh
%attr(755,root,root) %{dracutlibdir}/modules.d/90zfs/zfs-needshutdown.sh
%{dracutlibdir}/modules.d/90zfs/zfs-nonroot-necessities.service
%{dracutlibdir}/modules.d/90zfs/zfs-rollback-bootfs.service
%{dracutlibdir}/modules.d/90zfs/zfs-snapshot-bootfs.service
%{_mandir}/man7/dracut.zfs.7*

%files -n pam-pam_zfs_key
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_zfs_key.so

%if %{with python2}
%files -n python-pyzfs
%defattr(644,root,root,755)
%doc contrib/pyzfs/README
%{py_sitescriptdir}/libzfs_core
%{py_sitescriptdir}/pyzfs-*-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pyzfs
%defattr(644,root,root,755)
%doc contrib/pyzfs/README
%{py3_sitescriptdir}/libzfs_core
%{py3_sitescriptdir}/pyzfs-*-py*.egg-info
%endif
%endif

%if %{with kernel}
%files -n kernel-zfs-common-devel
%defattr(644,root,root,755)
%dir /usr/src/zfs-%{version}
/usr/src/zfs-%{version}/include
/usr/src/zfs-%{version}/zfs.release.in
/usr/src/zfs-%{version}/zfs_config.h.in
%endif
