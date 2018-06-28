%global with_debug 0

%if 0%{with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%global katadir %{_datadir}/kata-containers
%global katalibexecdir %{_libexecdir}/kata-containers

%global git0 https://github.com/kata-containers/osbuilder
%global commit0 ac0c29012fe2838bbb67cfc8f8d69454596af424
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name: kata-containers-image
Version: 1.0.0
Release: 1.git%{shortcommit0}%{?dist}
ExclusiveArch: %{ix86} x86_64
License: ASL 2.0
Summary: Kata Containers Image
URL: %{git0}
Source0: %{git0}/archive/%{commit0}/osbuilder-%{shortcommit0}.tar.gz
BuildRequires: git
BuildRequires: %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
Requires(post): %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
Requires(post): go-srpm-macros
Requires(post): qemu-img

%description
Kata Containers rootfs image

%prep
%autosetup -Sgit -n osbuilder-%{commit0}

%build

%install
install -dp %{buildroot}%{katadir}
install -dp %{buildroot}%{katalibexecdir}/{image-builder,initrd-builder,rootfs-builder,scripts}
install -p -m 755 rootfs-builder/rootfs.sh %{buildroot}%{katalibexecdir}/rootfs-builder/kata-rootfs_builder
install -p -m 644 rootfs-builder/versions.txt %{buildroot}%{katalibexecdir}/rootfs-builder/versions.txt
install -p -m 755 image-builder/image_builder.sh %{buildroot}%{katalibexecdir}/image-builder/kata-image_builder
install -p -m 755 initrd-builder/initrd_builder.sh %{buildroot}%{katalibexecdir}/initrd-builder/kata-initrd_builder
install -p -m 755 scripts/lib.sh %{buildroot}%{katalibexecdir}/scripts/lib.sh

for distro in alpine centos clearlinux euleros fedora
do
    install -dp %{buildroot}%{katalibexecdir}/rootfs-builder/$distro
    install -p -m 644 rootfs-builder/$distro/config.sh %{buildroot}%{katalibexecdir}/rootfs-builder/$distro
done

%post
echo "Creating Fedora image..."
GOPATH=%{gopath} OS_VERSION=%{?fedora} %{katalibexecdir}/rootfs-builder/kata-rootfs_builder fedora
GOPATH=%{gopath} %{katalibexecdir}/image-builder/kata-image_builder %{katalibexecdir}/rootfs-builder/rootfs-Fedora
GOPATH=%{gopath} %{katalibexecdir}/initrd-builder/kata-initrd_builder %{katalibexecdir}/rootfs-builder/rootfs-Fedora
mv /kata-* %{katadir}
rm -rf %{katalibexecdir}/rootfs-builder/rootfs-Fedora

%files
%dir %{katadir}
%dir %{katalibexecdir}
%dir %{katalibexecdir}/rootfs-builder
%dir %{katalibexecdir}/rootfs-builder/alpine
%dir %{katalibexecdir}/rootfs-builder/centos
%dir %{katalibexecdir}/rootfs-builder/clearlinux
%dir %{katalibexecdir}/rootfs-builder/euleros
%dir %{katalibexecdir}/rootfs-builder/fedora
%dir %{katalibexecdir}/image-builder
%dir %{katalibexecdir}/initrd-builder
%dir %{katalibexecdir}/scripts
%{katalibexecdir}/rootfs-builder/*
%{katalibexecdir}/image-builder/*
%{katalibexecdir}/initrd-builder/*
%{katalibexecdir}/scripts/*

%changelog
* Thu Jun 28 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-1.gitac0c290
- initial build
