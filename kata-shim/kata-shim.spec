%global DOMAIN github.com
%global ORG kata-containers
%global PROJECT shim
%global IMPORTNAME %{DOMAIN}/%{ORG}/%{PROJECT}
%global GO_VERSION 1.10.2

%if 0%{?suse_version}
%define LIBEXECDIR %{_libdir}
%else
%define LIBEXECDIR %{_libexecdir}
%endif

%undefine _missing_build_ids_terminate_build
Name:      kata-shim
Version:   1.0.0+git.74cbc1e
Release:   30.1
Summary  : No detailed summary available
Group    : Development/Tools
License  : Apache-2.0
Source0:   %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: git
Requires: kata-shim-bin

%global debug_package %{nil}

# Patches
#Patches


%description
.. contents::
.. sectnum::
``kata-shim``
===================
Overview
--------

%package bin
Summary: bin components for the kata-shim package.
Group: Binaries

%description bin
bin components for the kata-shim package.

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

%check
export http_proxy=http://127.0.0.1:9/
export https_proxy=http://127.0.0.1:9/
export no_proxy=localhost

%install
export GOROOT=$HOME/rpmbuild/BUILD/local/go
export PATH=$PATH:$HOME/rpmbuild/BUILD/local/go/bin
export GOPATH=$HOME/rpmbuild/BUILD/go/

make install LIBEXECDIR=%{buildroot}%{LIBEXECDIR}

%files
%defattr(-,root,root,-)

%files bin
%defattr(-,root,root,-)
%{LIBEXECDIR}/kata-containers
%{LIBEXECDIR}/kata-containers/kata-shim
