%define		mod_name	snake
Summary:	An Apache module to allow for Python plugins and control
Summary(pl):	Modu³ do Apache pozwalaj±cy na kontrolê i wtyczki Pythona
Name:		apache-mod_%{mod_name}
Version:	0.5.0
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	http://prdownloads.sourceforge.net/mod_%{mod_name}/mod_%{mod_name}-%{version}.tar.gz
URL:		http://modsnake.sourceforge.net/
BuildRequires:	/usr/sbin/apxs
BuildRequires:	apache-devel >= 1.3.15
BuildRequires:	python-devel >= 1.5
Prereq:		/usr/sbin/apxs
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(/usr/sbin/apxs -q LIBEXECDIR)

%description
mod_snake is an Apache module which allows for execution of Python
code directly within the Apache server process. By including an
interpreter in the Apache process, Python CGIs are accelerated, Python
can be embedded within HTML and Python written modules can control the
internals of the webserver.

%description -l pl
mod_snake to modu³ Apache pozwalaj±cy na wykonywanie kodu Pythona
bezpo¶rednio w procesie serwera Apache. W³±czaj±c interpreter do
procesu Apache skrypty CGI w Pythonie s± znacznie przyspieszone.
Python mo¿e byæ umieszczany w HTMLu oraz modu³y Pythona mog±
kontrolowaæ wewnêtrzne sprawy serwera www.

%prep 
%setup -q -n mod_%{mod_name}-%{version}

%build
%configure2_13 \
	--with-apxs=%{_sbindir}/apxs \
	--enable-dso
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	/usr/sbin/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*
