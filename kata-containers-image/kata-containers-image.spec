%global katadir %{_datadir}/kata-containers
%define agent_sha a099747
%define rootfs_os fedora
%global debug_package %{nil}
%global git0 https://github.com/kata-containers/osbuilder
%global commit0 72dca93263d6adc3d501d8404dd801a741381984
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name: kata-containers-image
Version: 1.0.0
Release: 1.git%{shortcommit0}%{?dist}
License: ASL 2.0
Summary: Kata Containers Image
URL: %{git0}
Source0: %{git0}/archive/%{commit0}/osbuilder-%{shortcommit0}.tar.gz
BuildRequires: qemu-img
BuildRequires: git
BuildRequires: %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
Kata Containers rootfs image

%prep
%autosetup -Sgit -n osbuilder-%{commit0}
chmod +x image-builder/image_builder.sh
chmod +x initrd-builder/initrd_builder.sh

%build
# build rootfs
sudo GOPATH=%{gopath} OS_VERSION=28 $(pwd)/rootfs-builder/rootfs.sh fedora

# build image
sudo GOPATH=%{gopath} $(pwd)/image-builder/image_builder.sh rootfs-builder/rootfs-Fedora

# build initrd
sudo GOPATH=%{gopath} $(pwd)/initrd-builder/initrd_builder.sh rootfs-builder/rootfs-Fedora

%install
ImageDir=%{buildroot}%{katadir}
mkdir -p ${ImageDir}

image=$(find ${PWD} -type f -name '*.img')
initrd=$(find ${PWD} -type f -name '*.initrd')
install -p "${image}" ${ImageDir}/
install -p "${initrd}"  ${ImageDir}/
ln -s %{katadir}/$(basename "${image}") ${ImageDir}/kata-containers.img
ln -s %{katadir}/$(basename "${initrd}")  ${ImageDir}/kata-containers-initrd.img

%files
%dir %{katadir}
%{katadir}/kata-containers-image*.img
%{katadir}/kata-containers.img
%{katadir}/kata-containers-initrd*.initrd
%{katadir}/kata-containers-initrd.img
