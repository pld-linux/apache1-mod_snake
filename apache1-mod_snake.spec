# NOTE
# - This project is RIP since Thu May 9 19:00:01 PDT 2002
# - and doesn't compile anyway
%define		mod_name	snake
%define 	apxs		/usr/sbin/apxs1
Summary:	An Apache module to allow for Python plugins and control
Summary(pl.UTF-8):	Moduł do Apache pozwalający na kontrolę i wtyczki Pythona
Name:		apache1-mod_%{mod_name}
Version:	0.5.0
Release:	1.2
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/mod%{mod_name}/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	7c043871a66a8579c6fec561c5d6cb84
Patch0:		%{name}-dumb_acam.patch
URL:		http://modsnake.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	python-devel >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache1 >= 1.3.33-2
Obsoletes:	apache-mod_snake <= 0.5.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
mod_snake is an Apache module which allows for execution of Python
code directly within the Apache server process. By including an
interpreter in the Apache process, Python CGIs are accelerated, Python
can be embedded within HTML and Python written modules can control the
internals of the webserver.

%description -l pl.UTF-8
mod_snake to moduł Apache pozwalający na wykonywanie kodu Pythona
bezpośrednio w procesie serwera Apache. Włączając interpreter do
procesu Apache skrypty CGI w Pythonie są znacznie przyspieszone.
Python może być umieszczany w HTML-u oraz moduły Pythona mogą
kontrolować wewnętrzne sprawy serwera WWW.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p0

%build
%configure2_13 \
	--with-apxs=%{apxs} \
	--enable-dso
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
