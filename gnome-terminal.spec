%define gettext_package gnome-terminal

%define glib2_version 2.2.0
%define pango_version 1.2.0
%define gtk2_version 2.2.0
%define libgnomeui_version 2.2.0
%define libgnome_version 2.2.0
#%define libzvt_version 1.113.0
%define vte_version 0.10.8
%define bonobo_activation_version 2.2.0
%define desktop_file_utils_version 0.2.90
%define startup_notification_version 0.5

Summary: GNOME Terminal
Name: gnome-terminal
Version: 2.2.1
Release: 3
URL: http://www.gnome.org/
Source0: ftp://ftp.gnome.org/pub/gnome/sources/gnome-terminal/2.1/gnome-terminal-%{version}.tar.bz2
License: GPL 
Group: User Interface/Desktops
BuildRoot: %{_tmppath}/%{name}-root

Requires: vte >= %{vte_version}
Requires: gtk2 >= 2.2.0
Requires: pango >= 1.2.0

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: libgnome-devel >= %{libgnome_version}
#BuildRequires: libzvt-devel >= %{libzvt_version}
BuildRequires: vte-devel >= %{vte_version}
BuildRequires: bonobo-activation-devel >= %{bonobo_activation_version}
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: startup-notification-devel >= %{startup_notification_version}

# Get the "same font as other applications" from the monospace_font
# GConf preference
Patch0: gnome-terminal-2.1.3-monospace.patch
Patch1: profterm-match-regex.patch

%description

GNOME terminal emulator application.

%prep
%setup -q
%patch0 -p1 -b .monospace
%patch1 -p0 -b .match-regex

%build

%configure --with-widget=vte
make

%install
rm -rf $RPM_BUILD_ROOT

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

desktop-file-install --vendor gnome --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  --add-only-show-in GNOME                                  \
  --add-category X-Red-Hat-Base                             \
  $RPM_BUILD_ROOT%{_datadir}/applications/*

rm -r $RPM_BUILD_ROOT/var/scrollkeeper

%find_lang %{gettext_package}

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gnome-terminal.schemas > /dev/null

%files -f %{gettext_package}.lang
%defattr(-,root,root)

%doc AUTHORS COPYING ChangeLog NEWS README

%{_bindir}/*
%{_datadir}/gnome-terminal
%{_datadir}/pixmaps
%{_datadir}/gnome
%{_datadir}/omf
%{_datadir}/applications
%{_sysconfdir}/gconf/schemas/gnome-terminal.schemas
%{_libdir}/bonobo

%changelog
* Fri Feb 14 2003 Havoc Pennington <hp@redhat.com> 2.2.1-3
- remove Xft buildreq

* Thu Feb  6 2003 Jeremy Katz <katzj@redhat.com> 2.2.1-2
- confusion about build roots abounds...

* Wed Feb  5 2003 Havoc Pennington <hp@redhat.com> 2.2.1-1
- 2.2.1

* Sun Jan 26 2003 Havoc Pennington <hp@redhat.com>
- require gtk 2.2, pango 1.2

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Havoc Pennington <hp@redhat.com>
- 2.2.0

* Fri Jan 10 2003 Havoc Pennington <hp@redhat.com>
- 2.1.4

* Tue Dec 10 2002 Havoc Pennington <hp@redhat.com>
- merge nalin's branch to HEAD, bump some dependency versions

* Tue Dec 10 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.3-0
- initial update to 2.1.3

* Tue Dec 10 2002 Tim Powers <timp@redhat.com> 2.0.1-6
- rebuild to fix broken deps on old libvte
- build on all arches

* Mon Sep  2 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.1-5
- fix goofy audible bell checkbox (backport from HEAD)

* Mon Sep  2 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.1-4
- fix incorrect regexp which matched newlines as parts of URLs (#71349)

* Fri Aug 23 2002 Jonathan Blandford <jrb@redhat.com>
- Clean up keyboard handling.

* Tue Aug 13 2002 Havoc Pennington <hp@redhat.com>
- require latest vte

* Thu Aug  8 2002 Havoc Pennington <hp@redhat.com>
- 2.0.1 released version instead of cvs snap
- clean up unpackaged files

* Thu Aug  8 2002 Nalin Dahyabhai <nalin@redhat.com>
- pick up widget padding

* Wed Jul 24 2002 Owen Taylor <otaylor@redhat.com>
- Use monospace preference for system font

* Thu Jul 18 2002 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Fri Jul 12 2002 Havoc Pennington <hp@redhat.com>
- 2.0.0.90 cvs snap

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jun 17 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Mon Jun 17 2002 Havoc Pennington <hp@redhat.com>
- 2.0.0
- use desktop-file-install
- put bonobo server file in file list
- put help files in file list
- apply some fixes from CVS (or rather, that I'm going to 
  check in to CVS soon)

* Fri Jun 14 2002 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in different environment

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


