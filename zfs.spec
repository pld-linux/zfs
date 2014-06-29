# TODO: PLDify init script
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)
#
%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif
%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif
Summary:	Native Linux port of the ZFS filesystem
Summary(pl.UTF-8):	Natywny linuksowy port systemu plików ZFS
%define	pname	zfs
Name:		%{pname}%{_alt_kernel}
Version:	0.6.3
%define	rel	1
Release:	%{rel}
License:	CDDL (ZFS), GPL v2+ (ZPIOS)
Group:		Applications/System
Source0:	http://archive.zfsonlinux.org/downloads/zfsonlinux/zfs/%{pname}-%{version}.tar.gz
# Source0-md5:	5bcc32c122934d421eba68e16826637d
Patch0:		%{name}-link.patch
URL:		http://zfsonlinux.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.26}
BuildRequires:	kernel%{_alt_kernel}-spl-devel >= 0.6.3
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
%if %{with userspace}
BuildRequires:	libblkid-devel
BuildRequires:	libselinux-devel
BuildRequires:	libuuid-devel
BuildRequires:	zlib-devel
%endif
Requires:	%{pname}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package -n kernel%{_alt_kernel}-zfs
Summary:	ZFS Linux kernel modules
Summary(pl.UTF-8):	ZFS - moduły jądra Linuksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-zfs
ZFS Linux kernel modules.

%description -n kernel%{_alt_kernel}-zfs -l pl.UTF-8
ZFS - moduły jądra Linuksa.

%package -n kernel%{_alt_kernel}-zfs-devel
Summary:	ZFS Linux kernel headers
Summary(pl.UTF-8):	ZFS - pliki nagłówkowe jądra Linuksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Development/Building
%{?with_dist_kernel:Requires:	kernel%{_alt_kernel}-headers}

%description -n kernel%{_alt_kernel}-zfs-devel
ZFS Linux kernel headers configured for PLD kernel%{_alt_kernel},
version %{_kernel_ver}.

%description -n kernel%{_alt_kernel}-zfs-devel -l pl.UTF-8
ZFS - pliki nagłówkowe jądra Linuksa skonfigurowane dla jądra PLD z
pakietu kernel%{_alt_kernel} w wersji %{_kernel_ver}.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--with-config="%{?with_kernel:%{?with_userspace:all}}%{!?with_kernel:user}%{!?with_userspace:kernel}" \
	--with-linux=%{_kernelsrcdir} \
	--with-systemdunitdir=%{systemdunitdir} \
	--with-systemdpresetdir=/etc/systemd/system-preset \
	--with-udevdir=/lib/udev

%{__make} \
	%{?with_verbose:V=1}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	DEFAULT_INIT_DIR=/etc/rc.d/init.d \
	INSTALL_MOD_DIR=misc

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc AUTHORS COPYRIGHT DISCLAIMER OPENSOLARIS.LICENSE README.markdown
%attr(755,root,root) /sbin/mount.zfs
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
%attr(754,root,root) /etc/rc.d/init.d/zfs
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

%files static
%defattr(644,root,root,755)
%{_libdir}/libnvpair.a
%{_libdir}/libuutil.a
%{_libdir}/libzfs.a
%{_libdir}/libzfs_core.a
%{_libdir}/libzpool.a

%files -n dracut-zfs
%defattr(644,root,root,755)
%doc dracut/README.dracut.markdown
%dir %{_libdir}/dracut/modules.d/90zfs
%attr(755,root,root) %{_libdir}/dracut/modules.d/90zfs/module-setup.sh
%attr(755,root,root) %{_libdir}/dracut/modules.d/90zfs/mount-zfs.sh
%attr(755,root,root) %{_libdir}/dracut/modules.d/90zfs/parse-zfs.sh
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-zfs
%defattr(644,root,root,755)
%dir /lib/modules/%{_kernel_ver}/misc/avl
/lib/modules/%{_kernel_ver}/misc/avl/zavl.ko*
%dir /lib/modules/%{_kernel_ver}/misc/nvpair
/lib/modules/%{_kernel_ver}/misc/nvpair/znvpair.ko*
%dir /lib/modules/%{_kernel_ver}/misc/unicode
/lib/modules/%{_kernel_ver}/misc/unicode/zunicode.ko*
%dir /lib/modules/%{_kernel_ver}/misc/zcommon
/lib/modules/%{_kernel_ver}/misc/zcommon/zcommon.ko*
%dir /lib/modules/%{_kernel_ver}/misc/zfs
/lib/modules/%{_kernel_ver}/misc/zfs/zfs.ko*
%dir /lib/modules/%{_kernel_ver}/misc/zpios
/lib/modules/%{_kernel_ver}/misc/zpios/zpios.ko*

%files -n kernel%{_alt_kernel}-zfs-devel
%defattr(644,root,root,755)
/usr/src/zfs-%{version}
%endif
