Summary: An SSL-encrypting socket wrapper.
Name: stunnel
Version: 4.05
Release: 4
License: GPL
Group: Applications/Internet
URL: http://stunnel.mirt.net/ 
Source0: ftp://stunnel.mirt.net/stunnel/stunnel-%{version}.tar.gz
Source1: ftp://stunnel.mirt.net/stunnel/stunnel-%{version}.tar.gz.asc
Source2: stunnel.cnf
Source3: Certificate-Creation
Source4: sfinger.xinetd
Source5: stunnel-sfinger.conf
Source6: pop3-redirect.xinetd
Source7: stunnel-pop3s-client.conf
Patch0: stunnel-4.02-authpriv.patch
Patch1: stunnel-4.05-nopem.patch
Patch2: stunnel-4.05-sample.patch
Buildroot: %{_tmppath}/stunnel-root
BuildPrereq: automake14, autoconf, openssl-devel, perl, pkgconfig,
BuildPrereq: tcp_wrappers, /usr/share/dict/words
Prereq: textutils, fileutils, /bin/mktemp, /sbin/ldconfig
Prereq: /usr/share/dict/words, /bin/hostname, /usr/bin/id, /usr/bin/getent
Requires: make

%description
Stunnel is a socket wrapper which can provide SSL (Secure Sockets
Layer) support to ordinary applications. For example, it can be used
in conjunction with imapd to create an SSL secure IMAP server.

%prep
%setup -q
%patch0 -p1 -b .authpriv
%patch1 -p1 -b .nopem
%patch2 -p1 -b .sample

iconv -f iso-8859-1 -t utf-8 < doc/stunnel.fr.8 > doc/stunnel.fr.8_
mv doc/stunnel.fr.8_ doc/stunnel.fr.8
iconv -f iso-8859-2 -t utf-8 < doc/stunnel.pl.8 > doc/stunnel.pl.8_
mv doc/stunnel.pl.8_ doc/stunnel.pl.8

aclocal-1.4
automake-1.4 -a
autoconf

%build
if pkg-config openssl ; then
	CFLAGS="$RPM_OPT_FLAGS `pkg-config --cflags openssl`"; export CFLAGS
	LDFLAGS="`pkg-config --libs-only-L openssl`"; export LDFLAGS
fi
%configure --with-tcp-wrappers
export tagname=CC
make LIBTOOL=%{_bindir}/libtool

%install
rm -rf $RPM_BUILD_ROOT
export tagname=CC
%makeinstall docdir=`pwd`/installed-docs LIBTOOL=%{_bindir}/libtool
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.so.?
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/stunnel/*sample*
# Move the translated man pages to the right subdirectories, and strip off the
# language suffixes.
for lang in fr pl ; do
	mkdir -p $RPM_BUILD_ROOT/%{_mandir}/${lang}/man8
	mv $RPM_BUILD_ROOT/%{_mandir}/man8/*.${lang}.8* $RPM_BUILD_ROOT/%{_mandir}/${lang}/man8/
	rename ".${lang}" "" $RPM_BUILD_ROOT/%{_mandir}/${lang}/man8/*
done

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc BUGS ChangeLog COPY* CREDITS NEWS PORTS README TODO doc/*.html
%doc $RPM_SOURCE_DIR/Certificate-Creation
%doc $RPM_SOURCE_DIR/sfinger.xinetd
%doc $RPM_SOURCE_DIR/pop3-redirect.xinetd
%doc $RPM_SOURCE_DIR/stunnel-pop3s-client.conf
%doc $RPM_SOURCE_DIR/stunnel-sfinger.conf
%doc tools/stunnel.conf-sample
%lang(en) %doc doc/en/*
%lang(po) %doc doc/pl/*
%{_libdir}/libstunnel.so
%{_mandir}/man8/stunnel.8*
%{_mandir}/*/man8/stunnel.8*
%{_sbindir}/stunnel
%dir %{_sysconfdir}/%{name}

%changelog
* Mon Nov 22 2004 Miloslav Trmac <mitr@redhat.com> - 4.05-4
- Convert man pages to UTF-8

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 27 2004 Nalin Dahyabhai <nalin@redhat.com> 4.05-2
- move the sample configuration to %%doc, it shouldn't be used as-is (#124373)

* Thu Mar 11 2004 Nalin Dahyabhai <nalin@redhat.com> 4.05-1
- update to 4.05

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Aug  7 2003 Elliot Lee <sopwith@redhat.com> 4.04-6
- Fix libtool

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Mar 21 2003 Nalin Dahyabhai <nalin@redhat.com> 4.04-4
- fix xinetd configuration samples

* Mon Feb 10 2003 Nalin Dahyabhai <nalin@redhat.com> 4.04-3
- rebuild

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Nalin Dahyabhai <nalin@redhat.com> 4.04-1
- update to 4.04

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 4.03-1
- use pkgconfig for information about openssl, if available

* Fri Jan  3 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.03

* Mon Oct 21 2002 Nalin Dahyabhai <nalin@redhat.com> 4.02-1
- update to 4.02

* Fri Oct  4 2002 Nalin Dahyabhai <nalin@redhat.com> 4.00-1
- don't create a dummy cert

* Wed Sep 25 2002 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.00
- remove textutils and fileutils as buildreqs, add automake/autoconf

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Nalin Dahyabhai <nalin@redhat.com> 3.22-2
- rebuild in new environment

* Wed Jan  2 2002 Nalin Dahyabhai <nalin@redhat.com> 3.22-1
- update to 3.22, correcting a format-string vulnerability

* Wed Oct 31 2001 Nalin Dahyabhai <nalin@redhat.com> 3.21a-1
- update to 3.21a

* Tue Aug 28 2001 Nalin Dahyabhai <nalin@redhat.com> 3.20-1
- log using LOG_AUTHPRIV facility by default (#47289)
- make permissions on stunnel binary 0755
- implicitly trust certificates in %%{_datadir}/ssl/trusted (#24034)

* Fri Aug 10 2001 Nalin Dahyabhai <nalin@redhat.com> 3.19-1
- update to 3.19 to avoid problems with stunnel being multithreaded, but
  tcp wrappers not being thrad-safe

* Mon Jul 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.17

* Mon Jul 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.16

* Mon Jul 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.15
- enable tcp-wrappers support

* Tue May 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- remove explicit requirement on openssl (specific version isn't enough,
  we have to depend on shared library version anyway)

* Fri Apr 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.14

* Mon Mar 26 2001 Preston Brown <pbrown@redhat.com>
- depend on make (#33148)

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Tue Feb  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.13 to get pthread, OOB, 64-bit fixes
- don't need sdf any more

* Thu Dec 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- pull in sdf to build the man page (#22892)

* Fri Dec 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.11
- chuck the SIGHUP patch (went upstream)
- chuck parts of the 64-bit clean patch (went upstream)

* Thu Dec 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.10
- more 64-bit clean changes, hopefully the last bunch

* Wed Dec 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- change piddir from the default /var/stunnel to /var/run
- clean out pid file on SIGHUP

* Fri Dec 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.9 to get a security fix

* Wed Oct 25 2000 Matt Wilson <msw@redhat.com>
- change all unsigned longs to u_int32_t when dealing with network
  addresses

* Fri Aug 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- make stunnel.pem also be (missingok)

* Thu Jun 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- move to Applications/Internet group
- clean up %post script
- make stunnel.pem %ghost %config(noreplace)
- provide a sample file for use with xinetd

* Thu Jun  8 2000 Nalin Dahyabhai <nalin@redhat.com>
- FHS compliance fixes
- modify defaults

* Tue Mar 14 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.8
- do not create certificate if one already exists

* Mon Feb 21 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.7
- add patch to find /usr/share/ssl
- change some perms

* Sat Oct 30 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Modify spec file to match Red Hat standards

* Fri Aug 12 1999 Damien Miller <damien@ibs.com.au>
- Updated to 3.4a
- Patched for OpenSSL 0.9.4
- Cleaned up files section

* Sun Jul 11 1999 Damien Miller <dmiller@ilogic.com.au>
- Updated to 3.3

* Sat Nov 28 1998 Damien Miller <dmiller@ilogic.com.au>
- Initial RPMification
