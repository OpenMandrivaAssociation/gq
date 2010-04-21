%define name	gq
%define version 1.3.4
%define release %mkrel 2
%define	Summary	GQ is a GTK-based LDAP client

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	%{Summary}
License:	GPL
Source0:	http://prdownloads.sourceforge.net/gqclient/%{name}-%{version}.tar.gz
Source11:	gq16.png
Source12:	gq32.png
Source13:	gq48.png
Patch1:		gq-1.3.4-mdv-fix-str-fmt.patch
Patch2:		gq-1.3.4-kerberos.patch
Patch3:		gq-1.3.4-configure.patch
URL:		http://biot.com/gq/
Group:		Databases
BuildRequires:	gettext-devel
BuildRequires:	krb5-devel
BuildRequires:	libsasl-devel
BuildRequires:	openldap-devel
BuildRequires:  libxml2-devel
BuildRequires:	glib-devel
BuildRequires:	gtk+2-devel
BuildRequires:	intltool
BuildRequires:	gnome-doc-utils >= 0.3.2
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libglade2.0-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
GQ is GTK+ LDAP client and browser utility. It can be used
for searching LDAP directory as well as browsing it using a
tree view.

%prep 
%setup -q
%patch1 -p1 -b .strfmt
%patch2 -p1 -b .kerberos
%patch3 -p0 -b .configure

%build 
#export CFLAGS="%{optflags} -DLDAP_DEPRECATED"
%configure2_5x \
    --with-default-codeset=UTF-8 \
    --enable-cache \
    --with-kerberos-prefix=%{_prefix} \
    --enable-browser-dnd \
    --disable-update-mimedb
%make

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=GQ
Comment=%{Summary}
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=GTK;Network;System;
EOF

#(peroyvind): replace menu with our own as it's more complete and valid ;)
rm -f %{buildroot}%{_datadir}/applications/gq.desktop

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

# Macro for locales
%find_lang %{name} --with-gnome --all-name

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr (-,root,root)
%doc AUTHORS ChangeLog NEWS README* TODO 
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/pixmaps/gq
%{_iconsdir}/hicolor/16x16/apps/*
%{_datadir}/mime/packages/gq-ldif.xml
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/omf/gq-manual/gq-manual-C.omf
%lang(de) %{_datadir}/omf/gq-manual/gq-manual-de.omf
