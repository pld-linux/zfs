# TODO:
# - PLDify init script
# - unpackaged initramfs-tools support:
#   /usr/share/initramfs-tools/conf-hooks.d/zfs
#   /usr/share/initramfs-tools/hooks/zfs
#   /usr/share/initramfs-tools/scripts/zfs
#
# Conditional build:
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
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

%define	rel	1
%define	pname	zfs
Summary:	Native Linux port of the ZFS filesystem
Summary(pl.UTF-8):	Natywny linuksowy port systemu plików ZFS
Name:		%{pname}%{?_pld_builder:%{?with_kernel:-kernel}}%{_alt_kernel}
Version:	0.6.5.8
Release:	%{rel}%{?_pld_builder:%{?with_kernel:@%{_kernel_ver_str}}}
License:	CDDL (ZFS), GPL v2+ (ZPIOS)
Group:		Applications/System
Source0:	https://github.com/zfsonlinux/zfs/releases/download/zfs-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ffc51dcf5260d3c7e747fe78f8ae307c
Patch0:		%{pname}-link.patch
Patch1:		x32.patch
URL:		http://zfsonlinux.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.701
%if %{with kernel}
%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2}
%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-spl-devel >= 0.6.3}
%endif
%if %{with userspace}
BuildRequires:	libblkid-devel
BuildRequires:	libselinux-devel
BuildRequires:	libuuid-devel
BuildRequires:	zlib-devel
%endif
Requires:	%{pname}-libs = %{version}-%{release}
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

%package -n kernel-zfs-common-devel
Summary:	ZFS Linux kernel headers
Summary(pl.UTF-8):	ZFS - pliki nagłówkowe jądra Linuksa
Group:		Development/Building

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
%dir /lib/modules/%{_kernel_ver}/misc/avl\
/lib/modules/%{_kernel_ver}/misc/avl/zavl.ko*\
%dir /lib/modules/%{_kernel_ver}/misc/nvpair\
/lib/modules/%{_kernel_ver}/misc/nvpair/znvpair.ko*\
%dir /lib/modules/%{_kernel_ver}/misc/unicode\
/lib/modules/%{_kernel_ver}/misc/unicode/zunicode.ko*\
%dir /lib/modules/%{_kernel_ver}/misc/zcommon\
/lib/modules/%{_kernel_ver}/misc/zcommon/zcommon.ko*\
%dir /lib/modules/%{_kernel_ver}/misc/zfs\
/lib/modules/%{_kernel_ver}/misc/zfs/zfs.ko*\
%dir /lib/modules/%{_kernel_ver}/misc/zpios\
/lib/modules/%{_kernel_ver}/misc/zpios/zpios.ko*\
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
%patch1 -p1

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
	--with-config="user" \
	--with-linux=%{_kernelsrcdir} \
	--with-systemdunitdir=%{systemdunitdir} \
	--with-systemdpresetdir=/etc/systemd/system-preset \
	--with-udevdir=/lib/udev

%{__make} \
	%{?with_verbose:V=1}
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

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
%{__mv} $RPM_BUILD_ROOT%{_npkgconfigdir}/* $RPM_BUILD_ROOT%{_pkgconfigdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc AUTHORS COPYRIGHT DISCLAIMER OPENSOLARIS.LICENSE README.markdown
%attr(755,root,root) /sbin/mount.zfs
%attr(755,root,root) %{_bindir}/arc_summary.py
%attr(755,root,root) %{_bindir}/arcstat.py
%attr(755,root,root) %{_bindir}/dbufstat.py
%attr(755,root,root) %{_sbindir}/fsck.zfs
%attr(755,root,root) %{_sbindir}/zdb
%attr(755,root,root) %{_sbindir}/zed
%attr(755,root,root) %{_sbindir}/zfs
%attr(755,root,root) %{_sbindir}/zhack
%attr(755,root,root) %{_sbindir}/zinject
%attr(755,root,root) %{_sbindir}/zpios
%attr(755,root,root) %{_sbindir}/zpool
%attr(755,root,root) %{_sbindir}/zstreamdump
%attr(755,root,root) %{_sbindir}/ztest
%dir %{_sysconfdir}/zfs
# package *.example as %doc? (they cannot act as default configuration)
%{_sysconfdir}/zfs/vdev_id.conf.*.example
%dir %{_sysconfdir}/zfs/zed.d
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zfs/zed.d/*.sh
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zfs/zed.d/zed.rc
%attr(754,root,root) /etc/rc.d/init.d/zfs-import
%attr(754,root,root) /etc/rc.d/init.d/zfs-mount
%attr(754,root,root) /etc/rc.d/init.d/zfs-share
%attr(754,root,root) /etc/rc.d/init.d/zfs-zed
%config(noreplace) %verify(not md5 mtime size) /etc/default/zfs
/etc/zfs/zfs-functions
/usr/lib/modules-load.d/zfs.conf
/etc/systemd/system-preset/50-zfs.preset
%{systemdunitdir}/zed.service
%{systemdunitdir}/zfs.target
%{systemdunitdir}/zfs-import-cache.service
%{systemdunitdir}/zfs-import-scan.service
%{systemdunitdir}/zfs-mount.service
%{systemdunitdir}/zfs-share.service
%attr(755,root,root) /lib/udev/vdev_id
%attr(755,root,root) /lib/udev/zvol_id
/lib/udev/rules.d/60-zvol.rules
/lib/udev/rules.d/69-vdev.rules
/lib/udev/rules.d/90-zfs.rules
%dir %{_libdir}/zfs
%dir %{_libdir}/zfs/zed.d
%attr(755,root,root) %{_libdir}/zfs/zed.d/*.sh
%dir %{_datadir}/zfs
%attr(755,root,root) %{_datadir}/zfs/*.sh
%dir %{_datadir}/zfs/zpios-profile
%attr(755,root,root) %{_datadir}/zfs/zpios-profile/*.sh
%dir %{_datadir}/zfs/zpios-test
%attr(755,root,root) %{_datadir}/zfs/zpios-test/*.sh
%dir %{_datadir}/zfs/zpool-config
%attr(755,root,root) %{_datadir}/zfs/zpool-config/*.sh
%{_mandir}/man1/zhack.1*
%{_mandir}/man1/zpios.1*
%{_mandir}/man1/ztest.1*
%{_mandir}/man5/vdev_id.conf.5*
%{_mandir}/man5/zfs-events.5*
%{_mandir}/man5/zfs-module-parameters.5*
%{_mandir}/man5/zpool-features.5*
%{_mandir}/man8/fsck.zfs.8*
%{_mandir}/man8/mount.zfs.8*
%{_mandir}/man8/vdev_id.8*
%{_mandir}/man8/zdb.8*
%{_mandir}/man8/zed.8*
%{_mandir}/man8/zfs.8*
%{_mandir}/man8/zinject.8*
%{_mandir}/man8/zpool.8*
%{_mandir}/man8/zstreamdump.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnvpair.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnvpair.so.1
%attr(755,root,root) %{_libdir}/libuutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libuutil.so.1
%attr(755,root,root) %{_libdir}/libzfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzfs.so.2
%attr(755,root,root) %{_libdir}/libzfs_core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzfs_core.so.1
%attr(755,root,root) %{_libdir}/libzpool.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzpool.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnvpair.so
%attr(755,root,root) %{_libdir}/libuutil.so
%attr(755,root,root) %{_libdir}/libzfs.so
%attr(755,root,root) %{_libdir}/libzfs_core.so
%attr(755,root,root) %{_libdir}/libzpool.so
%{_libdir}/libnvpair.la
%{_libdir}/libuutil.la
%{_libdir}/libzfs.la
%{_libdir}/libzfs_core.la
%{_libdir}/libzpool.la
%{_includedir}/libspl
%{_includedir}/libzfs
%{_pkgconfigdir}/libzfs.pc
%{_pkgconfigdir}/libzfs_core.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libnvpair.a
%{_libdir}/libuutil.a
%{_libdir}/libzfs.a
%{_libdir}/libzfs_core.a
%{_libdir}/libzpool.a

%files -n dracut-zfs
%defattr(644,root,root,755)
%doc contrib/dracut/README.dracut.markdown
%dir %{dracutlibdir}/modules.d/90zfs
%attr(755,root,root) %{dracutlibdir}/modules.d/90zfs/export-zfs.sh
%attr(755,root,root) %{dracutlibdir}/modules.d/90zfs/module-setup.sh
%attr(755,root,root) %{dracutlibdir}/modules.d/90zfs/mount-zfs.sh
%attr(755,root,root) %{dracutlibdir}/modules.d/90zfs/parse-zfs.sh
%attr(755,root,root) %{dracutlibdir}/modules.d/90zfs/zfs-lib.sh
%endif

%if %{with kernel}
%files -n kernel-zfs-common-devel
%defattr(644,root,root,755)
%dir /usr/src/zfs-%{version}
/usr/src/zfs-%{version}/include
/usr/src/zfs-%{version}/zfs.release.in
/usr/src/zfs-%{version}/zfs_config.h.in
%endif
