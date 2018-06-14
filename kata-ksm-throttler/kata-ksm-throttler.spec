%global with_debug 1

%define gobuild(o:) go build -tags="$BUILDTAGS rpm_crashtraceback" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};

%global provider github
%global provider_tld com
%global project kata-containers
%global repo ksm-throttler
%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}
%global commit0 aa4d33da7f6dc962e7fa67eee655f152a16c4bea
%global git0 https://%{import_path}
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
ExclusiveArch: x86_64
URL: %{git0}
Source0: %{git0}/archive/%{commit0}/%{repo}-%{shortcommit0}.tar.gz
Summary: Kata KSM throttling daemon
License: ASL 2.0
BuildRequires: %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires: git
BuildRequires: make
BuildRequires: systemd

%description
%{summary}

%prep
%autosetup -Sgit -n %{repo}-%{commit0}
for file in %{repo}.service.in vc-throttler.service.in
do
    sed -i "s|@libexecdir@|%{_libexecdir}|g" $file
    sed -i "s|@PACKAGE_NAME@|%{repo}|g" $file
    sed -i "s|@TARGET@|%{repo}|g" $file
    sed -i "s|@PACKAGE_URL@|%{import_path}|g" $file
    sed -i "s|@SERVICE_FILE@|%{repo}.service|g" $file
done

%build
mkdir _build
pushd _build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s $(dirs +1 -l) src/%{import_path}
popd

mv vendor src
export GOPATH=$(pwd)/_build:$(pwd):%{gopath}
GOPATH=$GOPATH %gobuild -o bin/%{repo} %{import_path}
GOPATH=$GOPATH %gobuild -o bin/kicker %{import_path}/trigger/kicker
GOPATH=$GOPATH %gobuild -o bin/vc %{import_path}/trigger/virtcontainers

%install
# install binaries
install -dp %{buildroot}%{_libexecdir}/%{repo}/trigger/virtcontainers
install -p -m 755 bin/%{repo} %{buildroot}%{_libexecdir}/%{repo}
install -p -m 755 bin/vc %{buildroot}%{_libexecdir}/%{repo}/trigger/virtcontainers

# install unitfiles
install -dp %{buildroot}%{_unitdir}
install -p -m 644 %{repo}.service.in %{buildroot}%{_unitdir}/%{repo}.service
install -p -m 644 vc-throttler.service.in %{buildroot}%{_unitdir}/vc-throttler.service

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md OWNERS README.md
%dir %{_libexecdir}/%{repo}
%{_libexecdir}/%{repo}/%{repo}
%dir %{_libexecdir}/%{repo}/trigger
%dir %{_libexecdir}/%{repo}/trigger/virtcontainers
%{_libexecdir}/%{repo}/trigger/virtcontainers/vc
%{_unitdir}/%{repo}.service
%{_unitdir}/vc-throttler.service

%changelog
* Thu Jun 14 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-1.gitaa4d33d
- first build (ready for Fedora review)
