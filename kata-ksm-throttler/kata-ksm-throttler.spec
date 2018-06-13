%global PREFIX /usr/
%global DOMAIN github.com
%global ORG kata-containers
%global PROJECT ksm-throttler
%global IMPORTNAME %{DOMAIN}/%{ORG}/%{PROJECT}
%global GO_VERSION 1.10.2
%global GO_ARCH amd64

%if 0%{?suse_version}
%define LIBEXECDIR %{_libdir}
%else
%define LIBEXECDIR %{_libexecdir}
%endif

%undefine _missing_build_ids_terminate_build
%define  debug_package %{nil}

Name:      kata-ksm-throttler
Version:   1.0.0.git+422c7f7
Release:   29.1
Source0:   %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Summary  : No detailed summary available
Group    : Development/Tools
License  : Apache-2.0

BuildRequires: git
BuildRequires: systemd
%if 0%{?suse_version} && 0%{?is_opensuse}
BuildRequires: openSUSE-release
%endif

# Patches
#Patches


%description
.. contents::
.. sectnum::
``kata-ksm-throttler``
===================
Overview
--------

%prep
mkdir local
tar -C local -xzf ../SOURCES/go%{GO_VERSION}.linux-%{GO_ARCH}.tar.gz

%setup -q
%autosetup -S git
#Apply patches


%build
export GOROOT=$HOME/rpmbuild/BUILD/local/go
export PATH=$PATH:$HOME/rpmbuild/BUILD/local/go/bin
export GOPATH=$HOME/rpmbuild/BUILD/go/

mkdir -p $HOME/rpmbuild/BUILD/go/src/%{DOMAIN}/%{ORG}
ln -s $HOME/rpmbuild/BUILD/kata-ksm-throttler-%{version} $HOME/rpmbuild/BUILD/go/src/%{IMPORTNAME}
cd $HOME/rpmbuild/BUILD/go/src/%{IMPORTNAME}
make \
    TARGET=kata-ksm-throttler \
    LIBEXECDIR=%{LIBEXECDIR}

%install
export GOROOT=$HOME/rpmbuild/BUILD/local/go
export PATH=$PATH:$HOME/rpmbuild/BUILD/local/go/bin
export GOPATH=$HOME/rpmbuild/BUILD/go/

cd $HOME/rpmbuild/BUILD/go/src/%{IMPORTNAME}
make install \
    TARGET=kata-ksm-throttler \
    DESTDIR=%{buildroot} \
    LIBEXECDIR=%{LIBEXECDIR}

%files
%defattr(-,root,root,-)
%{LIBEXECDIR}/kata-ksm-throttler
%{LIBEXECDIR}/kata-ksm-throttler/kata-ksm-throttler
%{LIBEXECDIR}/kata-ksm-throttler/trigger
%{LIBEXECDIR}/kata-ksm-throttler/trigger/virtcontainers
%{LIBEXECDIR}/kata-ksm-throttler/trigger/virtcontainers/vc
/usr/lib/systemd/system/kata-ksm-throttler.service
/usr/lib/systemd/system/vc-throttler.service
