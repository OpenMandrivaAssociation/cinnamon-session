%global po_package cinnamon-session-3.0
%global _internal_version  f2a4bea

Summary: Cinnamon session manager
Name:    cinnamon-session
Version: 2.4.2
Release: %mkrel 1
URL:     http://cinnamon.linuxmint.com

Source0: cinnamon-session-%{version}.tar.gz
#SourceGet0: https://github.com/linuxmint/cinnamon-session/archive/%{version}.tar.gz

License: GPLv2+ and LGPLv2+
Group:   Graphical desktop/Cinnamon

#Requires: system-logos
# Needed for cinnamon-settings-daemon
#Requires: cinnamon-control-center-filesystem

Requires: gsettings-desktop-schemas >= 0.1.7

# pull in dbus-x11, see bug 209924
Requires: dbus-x11

# we need an authentication agent in the fallback session
Requires: polkit-gnome

BuildRequires: pkgconfig(gtk+-3.0) >= 2.99.0
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(dbus-glib-1)
BuildRequires: pkgconfig(gnome-keyring-1)
BuildRequires: pkgconfig(libnotify) >= 0.7.0
BuildRequires: pkgconfig(pango)
BuildRequires: cinnamon-settings-daemon-devel
BuildRequires: desktop-file-utils
BuildRequires: pkgconfig(xau)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(xtrans)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(librsvg-2.0)
BuildRequires: pkgconfig(json-glib-1.0)

# this is so the configure checks find /usr/bin/halt etc.
BuildRequires: usermode

BuildRequires: pkgconfig(pangox)
BuildRequires: intltool
BuildRequires: gnome-common
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xt)
BuildRequires: pkgconfig(xtst)
BuildRequires: xmlto
BuildRequires: pkgconfig(upower-glib)
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(polkit-gobject-1)
BuildRequires: pkgconfig(libcanberra)

# an artificial requires to make sure we get dconf, for now
Requires: dconf

%description
Cinnamon-session manages a Cinnamon desktop or GDM login session. It starts up
the other core components and handles logout and saving the session.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
%configure2_5x --enable-docbook-docs \
           --docdir=%{_datadir}/doc/%{name} \
           --enable-systemd

make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

desktop-file-install                                     \
  --delete-original                                      \
  --set-icon=cinnamon-session-properties                 \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications          \
  $RPM_BUILD_ROOT%{_datadir}/applications/cinnamon-session-properties.desktop


%find_lang %{po_package}

%post
/usr/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  /usr/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%files -f %{po_package}.lang
%doc AUTHORS COPYING README
%doc %{_mandir}/man*/*
%{_datadir}/applications/cinnamon-session-properties.desktop
%{_bindir}/*
%{_libexecdir}/cinnamon-session-check-accelerated
%{_libexecdir}/cinnamon-session-check-accelerated-helper
%{_datadir}/cinnamon-session/
%{_datadir}/icons/hicolor/*/apps/cinnamon-session-properties.png
%{_datadir}/icons/hicolor/scalable/apps/cinnamon-session-properties.svg
%{_datadir}/glib-2.0/schemas/org.cinnamon.SessionManager.gschema.xml


%changelog
* Thu Nov 27 2014 joequant <joequant> 2.4.2-1.mga5
+ Revision: 799535
- upgrade to 2.4.2

* Sun Nov 23 2014 joequant <joequant> 2.4.1-1.mga5
+ Revision: 798403
- upgrade to 2.4

* Wed Oct 15 2014 umeabot <umeabot> 2.2.2-5.mga5
+ Revision: 743354
- Second Mageia 5 Mass Rebuild

* Tue Sep 16 2014 umeabot <umeabot> 2.2.2-4.mga5
+ Revision: 678400
- Mageia 5 Mass Rebuild

* Fri Sep 05 2014 joequant <joequant> 2.2.2-3.mga5
+ Revision: 672200
- remove polkit-desktop-policy requires

* Thu Sep 04 2014 joequant <joequant> 2.2.2-2.mga5
+ Revision: 671943
- rebuild with new systemd

* Sat Aug 30 2014 joequant <joequant> 2.2.2-1.mga5
+ Revision: 669423
- update to 2.2.2

* Thu May 15 2014 joequant <joequant> 2.2.1-1.mga5
+ Revision: 622874
- upgrade to 2.2.1

* Sat Apr 19 2014 joequant <joequant> 2.2.0-1.mga5
+ Revision: 616932
- upgrade to 2.2
- upgrade to 2.2

* Sun Mar 30 2014 joequant <joequant> 2.0.6-4.mga5
+ Revision: 610659
- upgrade to upower 1.0

  + dams <dams>
    - rebuild for new upower

* Wed Jan 08 2014 joequant <joequant> 2.0.6-2.mga4
+ Revision: 565561
- push to core/release

* Wed Jan 01 2014 joequant <joequant> 2.0.6-1.mga4
+ Revision: 563808
- upgrade to 2.0.6
- upgrade to 2.0.6

* Tue Dec 03 2013 colin <colin> 2.0.1-3.mga4
+ Revision: 554783
- Switch to mate-polkit for the fallback session authentication agent.

* Tue Oct 22 2013 umeabot <umeabot> 2.0.1-2.mga4
+ Revision: 542046
- Mageia 4 Mass Rebuild

* Mon Oct 14 2013 joequant <joequant> 2.0.1-1.mga4
+ Revision: 496767
- upgrade to 2.0.1

* Mon Oct 07 2013 joequant <joequant> 2.0.0-1.mga4
+ Revision: 492666
- fix patches
- update to 2.0.0

* Tue Oct 01 2013 joequant <joequant> 1.9.2-1.mga4
+ Revision: 490050
- update to 1.9.2

* Fri Aug 23 2013 joequant <joequant> 1.0.0-0.2.git58710ea.mga4
+ Revision: 470132
- fix requires

* Fri Aug 23 2013 joequant <joequant> 1.0.0-0.1.git58710ea.mga4
+ Revision: 470046
- imported package cinnamon-session

