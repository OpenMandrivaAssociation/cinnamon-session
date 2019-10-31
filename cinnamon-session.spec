%global po_package cinnamon-session-3.0
%global _internal_version  f2a4bea

Summary: Cinnamon session manager
Name:    cinnamon-session
Version: 4.2.1
Release: 1
URL:     http://cinnamon.linuxmint.com

Source0: https://github.com/linuxmint/cinnamon-session/archive/%{version}/%{name}-%{version}.tar.gz

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
BuildRequires: pkgconfig(xapp)
BuildRequires: xmlto
BuildRequires: pkgconfig(upower-glib)
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(polkit-gobject-1)
BuildRequires: pkgconfig(libcanberra)
BuildRequires:	meson

# an artificial requires to make sure we get dconf, for now
Requires: dconf

%description
Cinnamon-session manages a Cinnamon desktop or GDM login session. It starts up
the other core components and handles logout and saving the session.

%prep
%setup -q

%build
%meson -Dwith-gconf=false
#configure2_5x --enable-docbook-docs \
#          --docdir=%{_datadir}/doc/%{name} \
#          --enable-systemd --enable-compile-warnings=no

%meson_build

%install
%meson_install

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

%files
%doc AUTHORS COPYING README
%doc %{_mandir}/man*/*
%{_docdir}/cinnamon-session/dbus/cinnamon-session.html
%{_bindir}/*
%{_libexecdir}/cinnamon-session-check-accelerated
%{_libexecdir}/cinnamon-session-check-accelerated-helper
%{_datadir}/cinnamon-session/
%{_datadir}/icons/hicolor/*/apps/cinnamon-session-properties.png
%{_datadir}/icons/hicolor/scalable/apps/cinnamon-session-properties.svg
%{_datadir}/glib-2.0/schemas/org.cinnamon.SessionManager.gschema.xml


