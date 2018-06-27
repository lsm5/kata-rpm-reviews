%global debug_package %{nil}

%global commit_qemu 6ba2bfbee9a80bfd03605c5eb2ca743c8b68389e
%global shortcommit_qemu %(c=%{commit_qemu}; echo ${c:0:7})
%global git_qemu https://github.com/kata-containers/qemu

%global commit_capstone 22ead3e0bfdb87516656453336160e0a37b066bf
%global shortcommit_capstone %(c=%{commit_capstone}; echo ${c:0:7})
%global git_capstone https://github.com/qemu/capstone

%global commit_keycode 10739aa26051a5d49d88132604539d3ed085e72e
%global shortcommit_keycode %(c=%{commit_keycode}; echo ${c:0:7})
%global git_keycode https://github.com/qemu/keycodemapdb

Name: qemu-lite
Version: 2.11.0
Release: 1.git%{shortcommit_qemu}%{?dist}
URL: %{git_qemu}
ExclusiveArch: x86_64
Source0: %{git_qemu}/archive/%{commit_qemu}/qemu-%{shortcommit_qemu}.tar.gz
#Source0: qemu-lite-2.11.0+git.6ba2bfbee9.tar.gz
Source1: %{git_capstone}/archive/%{commit_capstone}/capstone-%{shortcommit_capstone}.tar.gz
Source2: %{git_keycode}/archive/%{commit_keycode}/keycodemapdb-%{shortcommit_keycode}.tar.gz
Source3: configure-hypervisor.sh
Patch1: 0001-memfd-fix-configure-test.patch
Summary: OpenBIOS development utilities
License: GPLv2
BuildRequires: automake
BuildRequires: bison
BuildRequires: capstone-devel
BuildRequires: flex
BuildRequires: gcc-c++
BuildRequires: git
BuildRequires: glib2-devel
BuildRequires: libattr-devel
BuildRequires: libcap-devel
BuildRequires: libcap-ng-devel
BuildRequires: librbd-devel
BuildRequires: libtool
BuildRequires: libtool-ltdl-devel
BuildRequires: m4
BuildRequires: make
BuildRequires: findutils
BuildRequires: numactl-devel
BuildRequires: python2-devel
BuildRequires: zlib-devel
BuildRequires: pkgconfig(pixman-1)
Requires: qemu-lite-bin
Requires: qemu-lite-data

%description
===========
QEMU is a generic and open source machine & userspace emulator and
virtualizer.

%package bin
Summary: bin components for the qemu-lite package.
Requires: qemu-lite-data

%description bin
bin components for the qemu-lite package.

%package data
Summary: data components for the qemu-lite package.

%description data
data components for the qemu-lite package.

%prep
%autosetup -Sgit -n qemu-%{commit_qemu}

tar zxf %{SOURCE1}
mv capstone-%{commit_capstone}/* capstone

tar zxf %{SOURCE2}
mv keycodemapdb-%{commit_keycode}/* ui/keycodemapdb

cp %{SOURCE3} .
#chmod +x configure-hypervisor.sh

%build
export LANG=C
bash "./configure-hypervisor.sh" "%{name}" \
	| xargs ./configure --prefix=%{_prefix} \
    --python=%{__python2} \
    --libdir=%{_libdir}/kata-%{name}

make V=1  %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
## make_install_append content
for file in %{buildroot}%{_bindir}/*
do
  dir=$(dirname "$file")
  bin=$(basename "$file")
  new=$(echo "$bin"|sed -e 's/qemu-/qemu-lite-/g' -e 's/ivshmem-/ivshmem-lite-/g' -e 's/virtfs-/virtfs-lite-/g')
  mv "$file" "$dir/$new"
done
## make_install_append end

%files bin
%{_bindir}/%{name}-ga
%{_bindir}/%{name}-pr-helper
%{_bindir}/%{name}-system-x86_64
%{_bindir}/virtfs-lite-proxy-helper
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/qemu-bridge-helper

%files data
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/qemu
%dir %{_datadir}/%{name}/qemu/keymaps
%{_datadir}/%{name}/qemu/*

%changelog
* Thu Jun 21 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.11.0.git6ba2bfb
- built 6ba2bfb
- Initial spec file grabbed from the srpm on OSBS
