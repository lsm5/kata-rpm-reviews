%global with_debug 1

%define gobuild(o:) go build -tags="$BUILDTAGS rpm_crashtraceback" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};

%global provider github
%global provider_tld com
%global project kata-containers
%global repo proxy
%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}
%global git0 https://%{import_path}
%global commit0 a69326b63802952b14203ea9c1533d4edb8c1d64
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%if 0%{with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif # with_debug

Name: kata-%{repo}
Version: 1.0.0
Release: 1.git%{shortcommit0}%{?dist}
ExclusiveArch: aarch64 %{arm} ppc64le s390x x86_64
URL: %{git0}
Source0: %{git0}/archive/%{commit0}/%{repo}-%{shortcommit0}.tar.gz
BuildRequires: %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires: git
Buildrequires: make
BuildRequires: systemd
Summary: Kata proxy
License: ASL 2.0

%description
%{summary}

%prep
%autosetup -Sgit -n %{repo}-%{commit0}

%build
mkdir _build
pushd _build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s $(dirs +1 -l) src/%{import_path}
popd

mv vendor src
export GOPATH=$(pwd)/_build:$(pwd):%{gopath}
GOPATH=$GOPATH %gobuild -o bin/%{name} %{import_path}

%install
# install binaries
install -dp %{buildroot}%{_libexecdir}/kata-containers
install -p -m 755 bin/%{name} %{buildroot}%{_libexecdir}/kata-containers

%clean

%files
%license LICENSE
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md README.md
%dir %{_libexecdir}/kata-containers
%{_libexecdir}/kata-containers/%{name}

%changelog
* Thu Jun 14 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-1.gita69326b
- first build (ready for Fedora review)
