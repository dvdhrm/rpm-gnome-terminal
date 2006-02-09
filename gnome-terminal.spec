%define gettext_package gnome-terminal

%define glib2_version 2.6.0
%define pango_version 1.8.0
%define gtk2_version 2.6.0
%define libgnomeui_version 2.3.0
#%define libzvt_version 1.113.0
%define vte_version 0.11.10
%define desktop_file_utils_version 0.2.90
%define startup_notification_version 0.8
%define libbonobo_version 2.3.0

Summary: GNOME Terminal
Name: gnome-terminal
Version: 2.13.90
Release: 2
URL: http://www.gnome.org/
Source0: gnome-terminal-%{version}.tar.bz2
Source1: ne.po
Patch0: gnome-terminal-2.12.0-inputmethod.patch
# fixed in 2.13.91
Patch1: gnome-terminal-2.13.90-invisible-char.patch
# fixed in 2.13.91
Patch2: gnome-terminal-2.13.90-link.patch
License: GPL 
Group: User Interface/Desktops

BuildRoot: %{_tmppath}/%{name}-root

Requires: vte >= %{vte_version}
Requires: gtk2 >= %{gtk2_version}
Requires: pango >= %{pango_version}

# gconftool-2
Requires: GConf2

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
#BuildRequires: libzvt-devel >= %{libzvt_version}
BuildRequires: vte-devel >= %{vte_version}
BuildRequires: libbonobo-devel >= %{libbonobo_version}
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: startup-notification-devel >= %{startup_notification_version}
BuildRequires: scrollkeeper gettext

# For intltool:
BuildRequires: perl-XML-Parser >= 2.31-16


%description

GNOME terminal emulator application.

%prep
%setup -q
cp ${RPM_SOURCE_DIR}/ne.po po
%patch0 -p1 -b .inputmethod
%patch1 -p0 -b .invisible-char
%patch2 -p1 -b .link

%build

#workaround broken perl-XML-Parser on 64bit arches
export PERL5LIB=/usr/lib64/perl5/vendor_perl/5.8.2 perl

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
%defattr(-,root,root,-)

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
* Thu Feb  9 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.90-2
- Re-add "Open Link" menuitems

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Christopher Aillon <caillon@redhat.com> 2.13.90-1
- Update to 2.13.90
- Add patch to not specify a default invisible char, let GTK+ handle it

* Thu Jan 19 2006 Matthias Clasen <mclasen@redhat.com> 2.13.3-1
- Update to 2.13.3

* Tue Jan 17 2006 Matthias Clasen <mclasen@redhat.com> 2.13.2-1
- Update to 2.13.2

* Fri Jan 13 2006 Matthias Clasen <mclasen@redhat.com> 2.13.1-1
- Update to 2.13.1
- Remove upstreamed patches

* Thu Jan  4 2006 Christopher Aillon <caillon@redhat.com> 2.13.0-2
- Revert patch from gnome bug 98715 to fix 176029, 176642

* Thu Dec 15 2005 Matthias Clasen <mclasen@redhat.com> 2.13.0-1
- Update to 2.13.0

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 28 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-2
- Respect the show_input_method_menu setting.

* Thu Sep  8 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-1
- Update to 2.12.0

* Tue Aug 16 2005 Warren Togami <wtogami@redhat.com> - 2.11.2-1
- rebuild for new cairo and 2.11.2

* Mon Jul 11 2005 Matthias Clasen <mclasen@redhat.com> 2.11.1-1
- Newer upstream version

* Wed May 4 2005 Ray Strode <rstrode@redhat.com> 2.10.0-2
- Fix ne translation (bug 152240).

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com> 2.10.0-1
- Update to 2.10.0

* Wed Feb  2 2005 Matthias Clasen <mclasen@redhat.com> 2.9.2-1
- Update to 2.9.2

* Thu Nov  4 2004 Ray Strode <rstrode@redhat.com> 2.8.0-2
- rebuild for rawhide

* Thu Nov  4 2004 Ray Strode <rstrode@redhat.com> 2.8.0-1
- Update to 2.8.0 (bug #136034)

* Fri Jul 30 2004 Ray Strode <rstrode@redhat.com> 2.7.3-1
- Update to 2.7.3

* Fri Jun 18 2004 Ray Strode <rstrode@redhat.com> 2.6.0-4
- patch a build busting type mismatch in libegg files

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 13 2004 Warren Togami <wtogami@redhat.com> 2.6.0-2
- #111015 BR scrollkeeper gettext

* Wed Mar 31 2004 Mark McLoughlin <markmc@redhat.com> 2.6.0-1
- Update to 2.6.0

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Alexander Larsson <alexl@redhat.com> 2.5.90-1
- update to 2.5.90

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Alexander Larsson <alexl@redhat.com> 2.5.1-1
- update to 2.5.1

* Wed Sep 17 2003 Alexander Larsson <alexl@redhat.com> 2.4.0.1-1
- update to 2.4.0.1

* Fri Aug 15 2003 Alexander Larsson <alexl@redhat.com> 2.3.1-1
- update to gnome 2.3

* Mon Jul 28 2003 Havoc Pennington <hp@redhat.com> 2.2.2-2
- rebuild

* Mon Jul  7 2003 Havoc Pennington <hp@redhat.com> 2.2.2-1
- 2.2.2
- require latest vte

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

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


