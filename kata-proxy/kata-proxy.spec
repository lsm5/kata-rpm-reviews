%global PREFIX /usr/
%global BINDIR %{PREFIX}/bin
%global DOMAIN github.com
%global ORG kata-containers
%global PROJECT proxy
%global IMPORTNAME %{DOMAIN}/%{ORG}/%{PROJECT}
%global GO_VERSION 1.10.2

%if 0%{?suse_version}
%define LIBEXECDIR %{_libdir}
%else
%define LIBEXECDIR %{_libexecdir}
%endif

%undefine _missing_build_ids_terminate_build
Name:      kata-proxy
Version:   1.0.0+git.a69326b
Release:   29.1
Source0:   %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pkgconfig(systemd)
BuildRequires: git
Summary  : No detailed summary available
Group    : Development/Tools
License  : Apache-2.0

Requires: kata-proxy-bin

#!BuildIgnore: post-build-checks

# Patches
#Patches


%description
.. contents::
.. sectnum::
``kata-proxy``
===================
Overview
--------

%global debug_package %{nil}
%define _unpackaged_files_terminate_build 0

%package bin
Summary: bin components for the kata-proxy package.
Group: Binaries

%description bin
bin components for the kata-proxy package.

%prep
mkdir local
tar -C local -xzf ../SOURCES/go%{GO_VERSION}.linux-amd64.tar.gz

%setup -q

# Patches
#Apply patches


%build
export GOROOT=$HOME/rpmbuild/BUILD/local/go
export PATH=$PATH:$HOME/rpmbuild/BUILD/local/go/bin
export GOPATH=$HOME/rpmbuild/BUILD/go/

mkdir -p $HOME/rpmbuild/BUILD/go/src/%{DOMAIN}/%{ORG}
ln -s %{_builddir}/%{name}-%{version} $HOME/rpmbuild/BUILD/go/src/%{IMPORTNAME}
cd $HOME/rpmbuild/BUILD/go/src/%{IMPORTNAME}
make

%clean
echo "Clean build root"
rm -rf %{buildroot}

%install
make install LIBEXECDIR=%{buildroot}%{LIBEXECDIR}

%files
%defattr(-,root,root,-)

%files bin
%defattr(-,root,root,-)
%{LIBEXECDIR}/kata-containers
%{LIBEXECDIR}/kata-containers/kata-proxy