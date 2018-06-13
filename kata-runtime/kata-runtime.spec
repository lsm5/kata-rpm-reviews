%global PREFIX /usr/
%global BINDIR %{PREFIX}/bin
%global DOMAIN github.com
%global ORG kata-containers
%global PROJECT runtime
%global IMPORTNAME %{DOMAIN}/%{ORG}/%{PROJECT}
%global GO_VERSION 1.10.2

%global DEFAULT_QEMU qemu-lite-system-x86_64

%if 0%{?suse_version}
%define LIBEXECDIR %{_libdir}
%else
%define LIBEXECDIR %{_libexecdir}
%endif

%undefine _missing_build_ids_terminate_build
%define  debug_package %{nil}

Name:      kata-runtime
# Version is expected to be started with a digit following by an alphanumeric string
# e.g. 1.0.0+git.1234567
Version:   1.0.0+git.086d197
Release:   41.1
Source0:   %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Summary  : No detailed summary available
Group    : Development/Tools
License  : Apache-2.0

BuildRequires: git
%if 0%{?suse_version} && 0%{?is_opensuse}
BuildRequires: openSUSE-release
%endif

%{!?el7 || !?suse_version:Requires: qemu-lite >= @qemu_lite_obs_fedora_version@ }

Requires: kata-containers-image >= 1.0.0-29
Requires: kata-linux-container >= 4.14.22.1-130
Requires: kata-proxy >= 1.0.0+git.a69326b-29
Requires: kata-shim >= 1.0.0+git.74cbc1e-30
Requires: kata-ksm-throttler >= 1.0.0+git.422c7f7-29
Requires: qemu-lite >= 2.11.0-43
Requires: qemu-vanilla >= 2.11-41

# Patches
#Patches


%description
.. contents::
.. sectnum::
``kata-runtime``
===================
Overview
--------

%prep
mkdir local
tar -C local -xzf ../SOURCES/go%{GO_VERSION}.linux-amd64.tar.gz
# Patches
#Apply patches


%setup -q
%autosetup -S git

%build
export GOROOT=$HOME/rpmbuild/BUILD/local/go
export PATH=$PATH:$HOME/rpmbuild/BUILD/local/go/bin
export GOPATH=$HOME/rpmbuild/BUILD/go/

mkdir -p $HOME/rpmbuild/BUILD/go/src/%{DOMAIN}/%{ORG}
ln -s $HOME/rpmbuild/BUILD/kata-runtime-%{version} $HOME/rpmbuild/BUILD/go/src/%{IMPORTNAME}
cd $HOME/rpmbuild/BUILD/go/src/%{IMPORTNAME}
make QEMUPATH=/usr/bin/%{DEFAULT_QEMU}

%check
export http_proxy=http://127.0.0.1:9/
export https_proxy=http://127.0.0.1:9/
export no_proxy=localhost

%install

export GOROOT=$HOME/rpmbuild/BUILD/local/go
export PATH=$PATH:$HOME/rpmbuild/BUILD/local/go/bin
export GOPATH=$HOME/rpmbuild/BUILD/go/

cd $HOME/rpmbuild/BUILD/go/src/%{IMPORTNAME}
make \
    DESTTARGET=%{buildroot}/usr/bin/kata-runtime \
    DESTCONFIG=%{buildroot}/usr/share/defaults/kata-containers/configuration.toml \
    SCRIPTS_DIR=%{buildroot}/usr/bin \
    QEMUPATH=/usr/bin/%{DEFAULT_QEMU} \
    install
sed -i -e '/^initrd =/d' %{buildroot}/usr/share/defaults/kata-containers/configuration.toml

%files
%defattr(-,root,root,-)
/usr/bin/kata-runtime
/usr/bin/kata-collect-data.sh
/usr/share/defaults/
/usr/share/defaults/kata-containers/
/usr/share/defaults/kata-containers/configuration.toml
