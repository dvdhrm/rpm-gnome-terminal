%define glib2_version 2.0.0
%define pango_version 1.0.99
%define gtk2_version 2.0.3-3
%define libgnomeui_version 1.117.2
%define libgnome_version 1.117.2
#%define libzvt_version 1.113.0
%define vte_version 0.4.0
%define bonobo_activation_version 1.0.0

Summary: GNOME Terminal
Name: gnome-terminal
Version: 1.9.7
Release: 10
URL: http://www.gnome.org
Source0: ftp://ftp.gnome.org/pub/GNOME/pre-gnome2/sources/gnome-terminal/%{name}-%{version}.tar.bz2
License: GPL 
Group: User Interface/Desktops
BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: libgnome-devel >= %{libgnome_version}
#BuildRequires: libzvt-devel >= %{libzvt_version}
BuildRequires: vte-devel >= %{vte_version}
BuildRequires: bonobo-activation-devel >= %{bonobo_activation_version}
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: Xft-devel
BuildRequires: fontconfig-devel

Patch0: gnome-terminal-1.9.7-monofont.patch
Patch1: gnome-terminal-1.9.7-vte-0.4.patch

%description

GNOME terminal emulator application.

%prep
%setup -q

%patch0 -p0 -b .monofont
%patch1 -p1 -b .vte-0.4

%build

%configure --with-widget=vte
make

%install
rm -rf $RPM_BUILD_ROOT

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gnome-terminal.schemas > /dev/null

%files -f %{name}.lang
%defattr(-,root,root)

%doc AUTHORS COPYING ChangeLog NEWS README

%{_bindir}/*
%{_datadir}/gnome-terminal
%{_datadir}/pixmaps
%{_datadir}/applications
%{_sysconfdir}/gconf/schemas/gnome-terminal.schemas

%changelog
* Thu Jun 18 2002 Nalin Dahyabhai <nalin@redhat.com>
- rebuild

* Fri Jun 14 2002 Nalin Dahyabhai <nalin@redhat.com>
- add patch to handle vte abi change

* Tue Jun 11 2002 Havoc Pennington <hp@redhat.com>
- add patch to get a decent default monospace font

* Mon Jun 10 2002 Havoc Pennington <hp@redhat.com>
- rebuild, had bin compat issues

* Sun Jun 09 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Sun Jun  9 2002 Havoc Pennington <hp@redhat.com>
- don't obsolete/provide gnome-core

* Fri Jun 07 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Wed Jun  5 2002 Havoc Pennington <hp@redhat.com>
- 1.9.7

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment
- build requires bonobo activation

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- 1.9.6.90
- provide gnome-core

* Fri May  3 2002 Havoc Pennington <hp@redhat.com>
- 1.9.5
- obsolete gnome-core

* Fri Apr 26 2002 Havoc Pennington <hp@redhat.com>
- 1.9.4.91, fixes scrollback thing

* Thu Apr 25 2002 Havoc Pennington <hp@redhat.com>
- 1.9.4.90
- move it to VTE, let's see how this goes

* Tue Apr 16 2002 Havoc Pennington <hp@redhat.com>
- Initial build.


