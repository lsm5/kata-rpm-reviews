%global debug_package %{nil}

%global commit0 6ba2bfbee9a80bfd03605c5eb2ca743c8b68389e
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global git0 https://github.com/kata-containers/qemu

Name: qemu-lite
Version: 2.11.0
Release: 1.git%{shortcommit0}%{?dist}
URL: %{git0}
#Source0: %%{git0}/archive/%%{commit0}/qemu-%%{shortcommit0}.tar.gz
Source0: qemu-lite-2.11.0+git.6ba2bfbee9.tar.gz
Source2: configure-hypervisor.sh
Patch1: 0001-memfd-fix-configure-test.patch
Summary: OpenBIOS development utilities
License: GPLv2 & BSD
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
%autosetup -Sgit -n qemu-lite-2.11.0+git.6ba2bfbee9
cp %{SOURCE2} .
chmod +x configure-hypervisor.sh

%build
export LANG=C
"./configure-hypervisor.sh" "%{name}" \
	| xargs ./configure --prefix=%{_prefix} \
    --python=%{__python2}

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
%{_datadir}/%{name}/qemu/QEMU,cgthree.bin
%{_datadir}/%{name}/qemu/QEMU,tcx.bin
%{_datadir}/%{name}/qemu/acpi-dsdt.aml
%{_datadir}/%{name}/qemu/bamboo.dtb
%{_datadir}/%{name}/qemu/bios-256k.bin
%{_datadir}/%{name}/qemu/bios.bin
%{_datadir}/%{name}/qemu/efi-e1000.rom
%{_datadir}/%{name}/qemu/efi-e1000e.rom
%{_datadir}/%{name}/qemu/efi-eepro100.rom
%{_datadir}/%{name}/qemu/efi-ne2k_pci.rom
%{_datadir}/%{name}/qemu/efi-pcnet.rom
%{_datadir}/%{name}/qemu/efi-rtl8139.rom
%{_datadir}/%{name}/qemu/efi-virtio.rom
%{_datadir}/%{name}/qemu/efi-vmxnet3.rom
%{_datadir}/%{name}/qemu/keymaps/ar
%{_datadir}/%{name}/qemu/keymaps/bepo
%{_datadir}/%{name}/qemu/keymaps/common
%{_datadir}/%{name}/qemu/keymaps/cz
%{_datadir}/%{name}/qemu/keymaps/da
%{_datadir}/%{name}/qemu/keymaps/de
%{_datadir}/%{name}/qemu/keymaps/de-ch
%{_datadir}/%{name}/qemu/keymaps/en-gb
%{_datadir}/%{name}/qemu/keymaps/en-us
%{_datadir}/%{name}/qemu/keymaps/es
%{_datadir}/%{name}/qemu/keymaps/et
%{_datadir}/%{name}/qemu/keymaps/fi
%{_datadir}/%{name}/qemu/keymaps/fo
%{_datadir}/%{name}/qemu/keymaps/fr
%{_datadir}/%{name}/qemu/keymaps/fr-be
%{_datadir}/%{name}/qemu/keymaps/fr-ca
%{_datadir}/%{name}/qemu/keymaps/fr-ch
%{_datadir}/%{name}/qemu/keymaps/hr
%{_datadir}/%{name}/qemu/keymaps/hu
%{_datadir}/%{name}/qemu/keymaps/is
%{_datadir}/%{name}/qemu/keymaps/it
%{_datadir}/%{name}/qemu/keymaps/ja
%{_datadir}/%{name}/qemu/keymaps/lt
%{_datadir}/%{name}/qemu/keymaps/lv
%{_datadir}/%{name}/qemu/keymaps/mk
%{_datadir}/%{name}/qemu/keymaps/modifiers
%{_datadir}/%{name}/qemu/keymaps/nl
%{_datadir}/%{name}/qemu/keymaps/nl-be
%{_datadir}/%{name}/qemu/keymaps/no
%{_datadir}/%{name}/qemu/keymaps/pl
%{_datadir}/%{name}/qemu/keymaps/pt
%{_datadir}/%{name}/qemu/keymaps/pt-br
%{_datadir}/%{name}/qemu/keymaps/ru
%{_datadir}/%{name}/qemu/keymaps/sl
%{_datadir}/%{name}/qemu/keymaps/sv
%{_datadir}/%{name}/qemu/keymaps/th
%{_datadir}/%{name}/qemu/keymaps/tr
%{_datadir}/%{name}/qemu/kvmvapic.bin
%{_datadir}/%{name}/qemu/linuxboot.bin
%{_datadir}/%{name}/qemu/linuxboot_dma.bin
%{_datadir}/%{name}/qemu/multiboot.bin
%{_datadir}/%{name}/qemu/openbios-ppc
%{_datadir}/%{name}/qemu/openbios-sparc32
%{_datadir}/%{name}/qemu/openbios-sparc64
%{_datadir}/%{name}/qemu/palcode-clipper
%{_datadir}/%{name}/qemu/petalogix-ml605.dtb
%{_datadir}/%{name}/qemu/petalogix-s3adsp1800.dtb
%{_datadir}/%{name}/qemu/ppc_rom.bin
%{_datadir}/%{name}/qemu/pxe-e1000.rom
%{_datadir}/%{name}/qemu/pxe-eepro100.rom
%{_datadir}/%{name}/qemu/pxe-ne2k_pci.rom
%{_datadir}/%{name}/qemu/pxe-pcnet.rom
%{_datadir}/%{name}/qemu/pxe-rtl8139.rom
%{_datadir}/%{name}/qemu/pxe-virtio.rom
%{_datadir}/%{name}/qemu/qemu-icon.bmp
%{_datadir}/%{name}/qemu/qemu_logo_no_text.svg
%{_datadir}/%{name}/qemu/s390-ccw.img
%{_datadir}/%{name}/qemu/sgabios.bin
%{_datadir}/%{name}/qemu/slof.bin
%{_datadir}/%{name}/qemu/spapr-rtas.bin
%{_datadir}/%{name}/qemu/trace-events-all
%{_datadir}/%{name}/qemu/u-boot.e500
%{_datadir}/%{name}/qemu/vgabios-cirrus.bin
%{_datadir}/%{name}/qemu/vgabios-qxl.bin
%{_datadir}/%{name}/qemu/vgabios-stdvga.bin
%{_datadir}/%{name}/qemu/vgabios-virtio.bin
%{_datadir}/%{name}/qemu/vgabios-vmware.bin
%{_datadir}/%{name}/qemu/vgabios.bin
%{_datadir}/%{name}/qemu/qemu_vga.ndrv
%{_datadir}/%{name}/qemu/s390-netboot.img
%{_datadir}/%{name}/qemu/skiboot.lid

%changelog
* Thu Jun 21 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.11.0.git6ba2bfb
- built 6ba2bfb
- Initial spec file grabbed from the srpm on OSBS
