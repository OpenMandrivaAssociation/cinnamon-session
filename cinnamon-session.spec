%global cinnamon_desktop_version 6.6.0

Summary: Cinnamon session manager
Name:    cinnamon-session
Version: 6.8.0
Release: 1
URL:     https://github.com/linuxmint/cinnamon-session/
Source0: https://github.com/linuxmint/cinnamon-session/archive/%{version}/%{name}-%{version}.tar.gz
License: GPLv2+ and LGPLv2+
Group:   Graphical desktop/Cinnamon

#Requires: system-logos
# Needed for cinnamon-settings-daemon
#Requires: cinnamon-control-center-filesystem

#Requires: gsettings-desktop-schemas >= 0.1.7

# pull in dbus-x11, see bug 209924
Requires: dbus-x11
# we need an authentication agent in the fallback session
#Requires: polkit-gnome

#Requires: cinnamon-translations >= 3.6.0
# an artificial requires to make sure we get dconf, for now
Requires: dconf
Requires: cinnamon-desktop >= %{cinnamon_desktop_version}

#BuildSystem:   meson

#BuildRequires: mold
BuildRequires: pkgconfig(gtk+-3.0) >= 3.0.0
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0) >= 2.37.3
BuildRequires: pkgconfig(libcanberra)
#BuildRequires: pkgconfig(dbus-1)
#BuildRequires: pkgconfig(dbus-glib-1)
#BuildRequires: pkgconfig(gnome-keyring-1)
#BuildRequires: pkgconfig(libnotify) >= 0.7.0
BuildRequires: pkgconfig(pango)
BuildRequires: pkgconfig(sm)
BuildRequires: pkgconfig(ice)           
BuildRequires: pkgconfig(x11)            
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xapp)
BuildRequires: pkgconfig(xau)
BuildRequires: pkgconfig(xtrans)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(cinnamon-desktop) >= %{cinnamon_desktop_version}
# BuildRequires: pkgconfig(cinnamon-settings-daemon) >= 6.0.0

#BuildRequires: desktop-file-utils
#BuildRequires: pkgconfig(xrandr)
#BuildRequires: pkgconfig(gl)
#BuildRequires: pkgconfig(librsvg-2.0)
#BuildRequires: pkgconfig(json-glib-1.0)
#BuildRequires: pkgconfig(gconf-2.0)
#BuildRequires: lib64glib2.0-devel

# this is so the configure checks find /usr/bin/halt etc.
#BuildRequires: usermode

BuildRequires: pkgconfig(pangox)
BuildRequires: pkgconfig(pangoxft) 
BuildRequires: intltool
BuildRequires: python 
#BuildRequires: gnome-common
#BuildRequires: pkgconfig(xt)
#BuildRequires: pkgconfig(xtst)
BuildRequires: xmlto
#BuildRequires: pkgconfig(upower-glib)
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(libsystemd)
#BuildRequires: pkgconfig(polkit-gobject-1)
BuildRequires: meson

%description
Cinnamon-session manages a Cinnamon desktop or GDM login session. It starts up the other core components and handles logout and saving the session.

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

%prep
%autosetup p1

%build
%meson

%meson_build

%install
%meson_install

%files
%doc AUTHORS COPYING README
%doc %{_mandir}/man*/*
%{_bindir}/*
/usr/lib/systemd/user/app-cinnamon-.scope.d/app-override.scope.conf
/usr/lib/systemd/user/dbus.service.d/dbus-override.service.conf
%{_libexecdir}/cinnamon-session-check-accelerated
%{_libexecdir}/cinnamon-session-check-accelerated-helper
%{_libexecdir}/cinnamon-session-binary
%{_datadir}/cinnamon-session/
%{_datadir}/icons/hicolor/*/apps/cinnamon-session-properties.png
%{_datadir}/icons/hicolor/scalable/apps/cinnamon-session-properties.svg
%{_datadir}/glib-2.0/schemas/org.cinnamon.SessionManager.gschema.xml
%{_userunitdir}/*.target
