#
# This is a special configuration of the Linux kernel, aimed exclusively
# for running inside a container
# This specialization allows us to optimize memory footprint and boot time.
#

%global bzimage_arch x86
%global kversion %{version}-%{release}.container

Name: kata-linux-container
Version: 4.14.22.1
Release: 1
License: GPL-2.0
Summary: The Linux kernel optimized for running inside a container
URL: http://www.kernel.org/
Group: kernel
Source0: https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.14.22.tar.xz
Source1: config
Patch1: 0001-NO-UPSTREAM-9P-always-use-cached-inode-to-fill-in-v9.patch
BuildRequires: bc
BuildRequires: binutils-devel
BuildRequires: pkgconfig(libelf)
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: flex
BuildRequires: bison

# don't strip .ko files!
%global __os_install_post %{nil}
%global debug_package %{nil}
%global __strip /bin/true

%description
%{summary}

%package debug
Summary: Debug components for the kata-linux-container package

%description debug
Debug components for the kata-linux-container package.
This package includes the kernel config and the kernel map.

%prep
%autosetup -Sgit -n linux-4.14.22
cp %{SOURCE1} .

%build
BuildKernel() {

    Arch=%{_arch}
    ExtraVer="-%{release}.container"

    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = ${ExtraVer}/" Makefile

    make -s mrproper
    cp config .config

    #Fedora uses gcc 8, build is failing due to warnings.
    export CFLAGS="-Wno-error=restrict"	 
    export EXTRA_CFLAGS="-Wno-format-truncation -Wno-cast-function-type -Wno-error=restrict -Wno-error"

    make -s ARCH=$Arch oldconfig > /dev/null
    make -s CONFIG_DEBUG_SECTION_MISMATCH=y %{?_smp_mflags} ARCH=$Arch %{?sparse_mflags} || exit 1
}

BuildKernel

%install

InstallKernel() {
    KernelImage=$1
    KernelImageRaw=$2

    Arch=%{_arch}
    KernelVer=%{kversion}
    KernelDir=%{buildroot}%{_datadir}/kata-containers

    mkdir   -p ${KernelDir}

    cp $KernelImage ${KernelDir}/vmlinuz-$KernelVer
    chmod 755 ${KernelDir}/vmlinuz-$KernelVer
    ln -sf vmlinuz-$KernelVer ${KernelDir}/vmlinuz.container

    cp $KernelImageRaw ${KernelDir}/vmlinux-$KernelVer
    chmod 755 ${KernelDir}/vmlinux-$KernelVer
    ln -sf vmlinux-$KernelVer ${KernelDir}/vmlinux.container

    cp .config "${KernelDir}/config-${KernelVer}"
    cp System.map "${KernelDir}/System.map-${KernelVer}"

    rm -f %{buildroot}/usr/lib/modules/$KernelVer/build
    rm -f %{buildroot}/usr/lib/modules/$KernelVer/source
}

InstallKernel arch/%{bzimage_arch}/boot/bzImage vmlinux

rm -rf %{buildroot}/usr/lib/firmware

%files
%dir %{_datadir}/kata-containers
%{_datadir}/kata-containers/vmlinux-%{kversion}
%{_datadir}/kata-containers/vmlinux.container
%{_datadir}/kata-containers/vmlinuz-%{kversion}
%{_datadir}/kata-containers/vmlinuz.container

%files debug
%defattr(-,root,root,-)
%{_datadir}/kata-containers/config-%{kversion}
%{_datadir}/kata-containers/System.map-%{kversion}
