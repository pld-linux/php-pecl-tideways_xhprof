#
# Conditional build:
%bcond_without	tests		# build without tests

%define		php_name	php%{?php_suffix}
%define		modname	tideways_xhprof
Summary:	%{modname} Tideways XHProf Extension
Name:		%{php_name}-pecl-%{modname}
Version:	5.0.4
Release:	1
License:	Apache v2.0
Group:		Development/Languages/PHP
Source0:	https://github.com/tideways/php-xhprof-extension/archive/v%{version}/%{modname}-%{version}.tar.gz
# Source0-md5:	68b68cd9410e62b8481445e0d89220c0
URL:		https://github.com/tideways/php-xhprof-extension
BuildRequires:	%{php_name}-cli
BuildRequires:	%{php_name}-devel >= 4:7.0
BuildRequires:	rpmbuild(macros) >= 1.666
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Modern XHProf compatible PHP Profiler.

%prep
%setup -qc
mv php-xhprof-extension-%{version}/* .

%build
phpize
%configure
%{__make}

# simple module load test
%{__php} -n -q \
	-d extension_dir=modules \
	-d extension=%{modname}.so \
	-m > modules.log
grep %{modname} modules.log

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md NOTICE
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
