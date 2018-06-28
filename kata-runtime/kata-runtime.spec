%global with_debug 1

%define gobuild(o:) go build -tags="$BUILDTAGS rpm_crashtraceback" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};

%global provider github
%global provider_tld com
%global project kata-containers
%global repo runtime
%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}
%global git0 https://%{import_path}
%global commit0 fca7eb822d29380502f38296b71b6e969253c4ee
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%if 0%{with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif # with_debug

%global DEFAULT_QEMU qemu-lite-system-x86_64

Name: kata-%{repo}
Version: 1.0.0
Release: 1.git%{shortcommit0}%{?dist}
Source0: %{git0}/archive/%{commit0}/%{repo}-%{commit0}.tar.gz
Summary: Kata runtime
License: ASL 2.0
BuildRequires: %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires: git
BuildRequires: make
Requires: kata-containers-image >= 1.0.0-1
Requires: kata-linux-container >= 4.14.22.1-130
Requires: kata-proxy >= 1.0.0-1
Requires: kata-shim >= 1.0.0-1
Requires: kata-ksm-throttler >= 1.0.0-2
Requires: qemu-lite >= 2.11.0-43
Requires: qemu

%description

%prep
%autosetup -Sgit -n %{repo}-%{commit0}

%build
make QEMUPATH=%{_bindir}/%{DEFAULT_QEMU}

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
    DESTTARGET=%{buildroot}%{_bindir}/kata-runtime \
    DESTCONFIG=%{buildroot}%{_datadir}/defaults/kata-containers/configuration.toml \
    SCRIPTS_DIR=%{buildroot}/%{_bindir} \
    QEMUPATH=%{_bindir}/%{DEFAULT_QEMU} \
    install
sed -i -e '/^initrd =/d' %{buildroot}%{_datadir}/defaults/kata-containers/configuration.toml

%files
%{_bindir}/%{name}
%{_bindir}/kata-collect-data.sh
%dir %{_datadir}/defaults
%dir %{_datadir}/defaults/kata-containers
%{_datadir}/defaults/kata-containers/configuration.toml
