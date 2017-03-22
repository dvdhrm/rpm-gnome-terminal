%define gettext_package gnome-terminal

%define glib2_version 2.42.0
%define gtk3_version 3.20.0
%define vte_version 0.48.0
%define desktop_file_utils_version 0.2.90

Name: gnome-terminal
Version: 3.24.0
Release: 1%{?dist}
Summary: Terminal emulator for GNOME

License: GPLv3+ and GFDL
URL: http://www.gnome.org/
Source0: http://download.gnome.org/sources/gnome-terminal/3.24/gnome-terminal-%{version}.tar.xz
Source1: org.gnome.Terminal.gschema.override

Patch0: 0001-build-Don-t-treat-warnings-as-errors.patch

Patch100: gnome-terminal-notify-open-title-transparency.patch

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: gsettings-desktop-schemas-devel
BuildRequires: vte291-devel >= %{vte_version}
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: gnome-common
BuildRequires: autoconf automake libtool
BuildRequires: itstool
BuildRequires: dconf-devel
BuildRequires: libuuid-devel
BuildRequires: nautilus-devel
BuildRequires: gnome-shell
BuildRequires: appdata-tools
BuildRequires: pcre2-devel
BuildRequires: systemd
BuildRequires: vala-devel

Requires: dbus-x11
Requires: glib2%{?_isa} >= %{glib2_version}
Requires: gsettings-desktop-schemas
Requires: gtk3%{?_isa} >= %{gtk3_version}
Requires: vte291%{?_isa} >= %{vte_version}

%description
gnome-terminal is a terminal emulator for GNOME. It features the ability to use
multiple terminals in a single window (tabs) and profiles support.

%package nautilus
Summary: GNOME Terminal extension for Nautilus
Requires: %{name}%{?_isa} = %{version}-%{release}

Provides: nautilus-open-terminal = %{version}-%{release}
Obsoletes: nautilus-open-terminal < 0.20-8

%description nautilus
This package provides a Nautilus extension that adds the 'Open in Terminal'
option to the right-click context menu in Nautilus.

%prep
%setup -q
%patch0 -p1 -b .warnings
%patch100 -p1 -b .notify-open-title-transparency

%build
autoreconf -f -i
%configure --disable-static --disable-gterminal --disable-migration --with-gtk=3.0 --with-nautilus-extension

make %{?_smp_mflags}

%install
%make_install

rm -f $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-3.0/*.la

cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas

%find_lang %{gettext_package} --with-gnome

%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/org.gnome.Terminal.desktop

%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{gettext_package}.lang
%license COPYING
%doc AUTHORS NEWS

%{_bindir}/gnome-terminal
%{_datadir}/metainfo/org.gnome.Terminal.appdata.xml
%{_datadir}/applications/org.gnome.Terminal.desktop
%{_libexecdir}/gnome-terminal-server
%{_datadir}/dbus-1/services/org.gnome.Terminal.service
%{_datadir}/glib-2.0/schemas/org.gnome.Terminal.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.Terminal.gschema.override
%{_datadir}/gnome-shell
%{_userunitdir}/gnome-terminal-server.service

%files nautilus
%{_libdir}/nautilus/extensions-3.0/libterminal-nautilus.so
%{_datadir}/metainfo/org.gnome.Terminal.Nautilus.metainfo.xml

%changelog
* Wed Mar 22 2017 Kalev Lember <klember@redhat.com> - 3.24.0-1
- Update to 3.24.0
- Rebase the translations

* Mon Feb 27 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.23.90-1
- Update to 3.23.90
- Update translations
- Ensure that the transparency scale is sensitive only when a transparent
  background is used
- Rebase transparency, command-notify and translation patches

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 15 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.22.1-2
- Backport fix for search-provider crash (RH #1398958)
- Update translations

* Tue Nov 08 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.22.1-1
- Update to 3.22.1
- Rebase the translations
- Restore custom terminal titles
- Restore separate menuitems for opening tabs and windows

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0
- Rebase the translations

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 3.21.92-1
- Update to 3.21.92
- Rebase the translations
- Don't set group tags
- Use make_install macro

* Fri Aug 19 2016 Kalev Lember <klember@redhat.com> - 3.21.90-2
- Backport a patch to fix terminal shrinking with every line entered

* Thu Aug 18 2016 Kalev Lember <klember@redhat.com> - 3.21.90-1
- Update to 3.21.90
- Rebase the translations

* Wed Jun 01 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.20.2-2
- Add Provides/Obsoletes to replace nautilus-open-terminal

* Wed May 11 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.20.2-1
- Update to 3.20.2

* Tue May 10 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.20.1-2
- Rebuild against vte291 ABI fix

* Mon Apr 11 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.20.1-1
- Update to 3.20.1
- Rebase the translations

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0
- Rebase the translations

* Thu Mar 17 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.19.92-1
- Update to 3.19.92
- Rebase the translations

* Thu Mar 03 2016 Kalev Lember <klember@redhat.com> - 3.19.91-1
- Update to 3.19.91
- Rebase transparency, command-notify and translation patches

* Thu Feb 18 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.19.2-1
- Update to 3.19.2
- Rebase the translations

* Thu Feb 18 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.19.1-2
- Adjust the dark terminal override to match the new setting

* Thu Feb 11 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.19.1-1
- Update to 3.19.1
- Rebase transparency, command-notify and translation patches
- Dark terminals have been restored upstream

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 13 2015 Debarshi Ray <rishi@fedoraproject.org> - 3.18.2-1
- Update to 3.18.2
- Consolidate all downstream features into a single patch to avoid conflicts
- Rebase the translations

* Thu Nov 12 2015 Owen Taylor <otaylor@redhat.com> - 3.18.1-3
- Add patch fixing transparent mode under Wayland

* Sat Oct 31 2015 Kalev Lember <klember@redhat.com> - 3.18.1-2
- Drop GConf migrator for F24 (#1276525)

* Wed Oct 14 2015 Kalev Lember <klember@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Wed Oct 07 2015 Debarshi Ray <rishi@fedoraproject.org> - 3.18.0-1
- Update to 3.18.0
- Backport a few upstream fixes
- Rebase the translations

* Thu Oct 01 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 3.17.91-2
- Use a symbolic new tab icon

* Mon Sep 14 2015 Debarshi Ray <rishi@fedoraproject.org> - 3.17.91-1
- Update to 3.17.91
- Restore translations for dark variant strings
- Rebase the translations for transparency strings

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 12 2015 Debarshi Ray <rishi@fedoraproject.org> - 3.16.2-1
- Update to 3.16.2
- Rebase the translations for transparency strings

* Tue Apr 14 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1-1
- Update to 3.16.1

* Tue Mar 24 2015 Debarshi Ray <rishi@fedoraproject.org> - 3.16.0-1
- Update to 3.16.0
- Rebase the translations for transparency strings

* Tue Mar 17 2015 Debarshi Ray <rishi@fedoraproject.org> - 3.15.92-1
- Update to 3.15.92
- Drop upstreamed patch
- Rebase the translations for transparency strings

* Mon Mar 16 2015 Debarshi Ray <rishi@fedoraproject.org> - 3.15.90-2
- Withdraw the notification on focus-in-event

* Wed Feb 18 2015 Debarshi Ray <rishi@fedoraproject.org> - 3.15.90-1
- Update to 3.15.90
- Restore translations for transparency strings
- Restore dark terminals
- Add command-notify patches

* Mon Jan 26 2015 Adam Williamson <awilliam@redhat.com> - 3.14.2-2
- backport partial fix for BGO#743395

* Mon Nov 10 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.2-1
- Update to 3.14.2

* Mon Oct 13 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.1-1
- Update to 3.14.1

* Sun Sep 21 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Sun Sep 14 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-1
- Update to 3.13.92

* Fri Sep 12 2014 Debarshi Ray <rishi@fedorapeople.org> - 3.13.90-2
- Restore transparency

* Tue Aug 19 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.90-1
- Update to 3.13.90

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 24 2014 Richard Hughes <rhughes@redhat.com> - 3.13.2-1
- Update to 3.13.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-1
- Update to 3.13.1

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.0-2
- Fix parent class in template definition

* Sun Apr 27 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.0-1
- Update to 3.13.0

* Sat Apr 26 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-1
- Update to 3.12.1

* Thu Apr 03 2014 Debarshi Ray <rishi@fedoraproject.org> - 3.12.0-2
- Use the dark theme variant

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Mon Mar 10 2014 Kevin Fenzi <kevin@scrye.com> 3.11.3-2
- Rebuild for new gnome-shell
- Own datadir/gnome-shell for search provider

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Mon Nov 25 2013 Richard Hughes <rhughes@redhat.com> - 3.11.0-2
- Re-issued tarball. Kinda unusual, but such is life.

* Tue Nov 19 2013 Richard Hughes <rhughes@redhat.com> - 3.11.0-1
- Update to 3.11.0

* Thu Nov 14 2013 Richard Hughes <rhughes@redhat.com> - 3.10.2-1
- Update to 3.10.2

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90
- Package up the nautilus extension in gnome-terminal-nautilus subpackage

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul  8 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.4-1
- Update to 3.8.4
- Fixes a crash on session resume (#981440)

* Mon Jun 10 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.3-1
- Update to 3.8.3
- Use desktop-file-validate instead of desktop-file-install

* Mon May 13 2013 Richard Hughes <rhughes@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Tue Apr 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0.1-1
- Update to 3.8.0.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Thu Mar  7 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Tue Feb 26 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.2-3
- Bring back titlebars on maximized terminals

* Fri Jan 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.2-2
- Backport a fix for a crash in terminal_screen_container_style_updated

* Fri Jan 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.2-1
- Update to 3.7.2

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 3.7.1-1
- Update to 3.7.1

* Wed Jan 09 2013 Richard Hughes <hughsient@gmail.com> - 3.7.0-1
- Update to 3.7.0

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1.1-1
- Update to 3.4.1.1

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0.1-1
- Update to 3.4.0.1
- Avoid listing files twice in %%files

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.0-1
- Update to 3.3.0

* Thu Jan 12 2012 Matthias Clasen <mclasen@redhat.com> - 3.2.1-2
- Update license field (#639132)

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Apr 25 2011 Matthias Clasen <mclasen@redhat.com> 3.0.1-1
- Update to 3.0.1

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> 3.0.0-1
- Update to 3.0.0

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> 2.33.90-1
- Update to 2.33.90

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 2.33.5-3
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.5-1
- Update to 2.33.5

* Wed Jan 12 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.4-2
- Make the find dialog work again

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.4-1
- Update to 2.33.4

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.3-1
- Update to 2.33.3

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.33.2-2
- Rebuild against new gtk

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.33.2-1
- Update to 2.33.2
- Back to gtk3

* Fri Oct  8 2010 Owen Taylor <otaylor@redhat.com> - 2.33.0-3
- Revert back to a gtk2 build - the gtk3 build has major sizing issues
  (rhbz #641337)

* Thu Oct  7 2010 Matthias Clasen <mclasen@redhat.com> - 2.33.0-2
- Build against gtk3

* Mon Oct  4 2010 Matthias Clasen <mclasen@redhat.com> - 2.33.0-1
- Update to 2.33.0

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.91-1
- Update to 2.31.91

* Thu Aug 19 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.90-1
- Update to 2.31.90

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.3-1
- Update to 2.31.3

* Tue May  4 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.2-2
- Add more translations for search UI

* Tue May  4 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.2-1
- Update to 2.31.2
- Add translations for search UI

* Tue May  4 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.1-1
- Update to 2.31.1

* Mon Apr 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.1-1
- Update to 2.30.1

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Thu Mar 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.92-1
- Update to 2.29.92

* Sun Feb 14 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.6-3
- Add missing libs

* Thu Jan 14 2010 Behdad Esfahbod <behdad@redhat.com> - 2.29.6-2
- Second try
- Drop stale patch

* Thu Jan 14 2010 Behdad Esfahbod <behdad@redhat.com> - 2.29.6-1
- Update to 2.29.6
