%define version 1.0.0
%define release 29
%define agent_sha a099747
%define rootfs_os clearlinux

Name:           kata-containers-image
Version:        %{version}
Release:        %{release}.1
License:        Artistic-1.0 BSD-3-Clause BSD-3-Clause-Kata BSD-4-Clause-UC GFDL-1.3 GPL-2.0 GPL-2.0+ GPL-3.0 GPL-3.0+ LGPL-2.0 LGPL-2.0+ LGPL-2.1 LGPL-3.0+ MIT MPL-2.0 Public-Domain 
Summary:        Kata Containers Image
Url:            https://github.com/kata-containers/osbuilder
Group:          image
Source0:        kata-containers.tar.gz
Source1:        LICENSE

%global debug_package %{nil}

#Patches


%description
Kata Containers rootfs image

%prep
# Patches
#Apply patches


%install
ImageDir=%{buildroot}/usr/share/kata-containers
mkdir -p ${ImageDir}

pushd %{_sourcedir}
tar xfz kata-containers.tar.gz
image=$(find ${PWD} -type f -name '*.img')
initrd=$(find ${PWD} -type f -name '*.initrd')
popd
install -p "${image}" ${ImageDir}/
install -p "${initrd}"  ${ImageDir}/
ln -s /usr/share/kata-containers/$(basename "${image}") ${ImageDir}/kata-containers.img
ln -s /usr/share/kata-containers/$(basename "${initrd}")  ${ImageDir}/kata-containers-initrd.img

%files
%if 0%{?suse_version}
%dir /usr/share/kata-containers
%endif
/usr/share/kata-containers/kata-containers-image*.img
/usr/share/kata-containers/kata-containers.img
/usr/share/kata-containers/kata-containers-initrd*.initrd
/usr/share/kata-containers/kata-containers-initrd.img
