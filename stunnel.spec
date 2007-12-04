Summary: An SSL-encrypting socket wrapper
Name: stunnel
Version: 4.20
Release: 5
License: GPLv2
Group: Applications/Internet
URL: http://stunnel.mirt.net/
Source0: ftp://stunnel.mirt.net/stunnel/stunnel-%{version}.tar.gz
Source1: ftp://stunnel.mirt.net/stunnel/stunnel-%{version}.tar.gz.asc
Source2: Certificate-Creation
Source3: sfinger.xinetd
Source4: stunnel-sfinger.conf
Source5: pop3-redirect.xinetd
Source6: stunnel-pop3s-client.conf
Patch0: stunnel-4.08-authpriv.patch
Patch1: stunnel-4.18-sample.patch
Buildroot: %{_tmppath}/stunnel-root
# util-linux is needed for rename
BuildRequires: openssl-devel, pkgconfig, tcp_wrappers-devel, util-linux

%description
Stunnel is a socket wrapper which can provide SSL (Secure Sockets
Layer) support to ordinary applications. For example, it can be used
in conjunction with imapd to create an SSL secure IMAP server.

%prep
%setup -q
%patch0 -p1 -b .authpriv
%patch1 -p1 -b .sample

iconv -f iso-8859-1 -t utf-8 < doc/stunnel.fr.8 > doc/stunnel.fr.8_
mv doc/stunnel.fr.8_ doc/stunnel.fr.8
iconv -f iso-8859-2 -t utf-8 < doc/stunnel.pl.8 > doc/stunnel.pl.8_
mv doc/stunnel.pl.8_ doc/stunnel.pl.8

%build
CFLAGS="$RPM_OPT_FLAGS -fPIC"; export CFLAGS
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`";
	LDFLAGS="`pkg-config --libs-only-L openssl`"; export LDFLAGS
fi
%configure --enable-ipv6 \
	CPPFLAGS="-UPIDFILE -DPIDFILE='\"%{_localstatedir}/run/stunnel.pid\"'"
make LDADD="-pie -Wl,-z,defs,-z,relro"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/stunnel
touch $RPM_BUILD_ROOT%{_sysconfdir}/stunnel/stunnel.pem
make install DESTDIR=$RPM_BUILD_ROOT
# Move the translated man pages to the right subdirectories, and strip off the
# language suffixes.
for lang in fr pl ; do
	mkdir -p $RPM_BUILD_ROOT/%{_mandir}/${lang}/man8
	mv $RPM_BUILD_ROOT/%{_mandir}/man8/*.${lang}.8* $RPM_BUILD_ROOT/%{_mandir}/${lang}/man8/
	rename ".${lang}" "" $RPM_BUILD_ROOT/%{_mandir}/${lang}/man8/*
done

mkdir srpm-docs
cp %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} srpm-docs

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog COPY* CREDITS NEWS PORTS README TODO
%doc tools/stunnel.conf-sample
%doc srpm-docs/*
%lang(en) %doc doc/en/*
%lang(po) %doc doc/pl/*
%exclude %{_datadir}/doc/stunnel
%{_libdir}/libstunnel.so
%exclude %{_libdir}/libstunnel.la
%{_mandir}/man8/stunnel.8*
%lang(fr) %{_mandir}/fr/man8/stunnel.8*
%lang(pl) %{_mandir}/pl/man8/stunnel.8*
%{_sbindir}/stunnel
%{_sbindir}/stunnel3
%dir %{_sysconfdir}/%{name}
%exclude %{_sysconfdir}/stunnel/*

%changelog
* Tue Dec  4 2007 Miloslav Trmač <mitr@redhat.com> - 4.20-5
- Rebuild with openssl-0.9.8g

* Tue Oct 16 2007 Miloslav Trmač <mitr@redhat.com> - 4.20-4
- Revert the port to NSS, wait for NSS-based stunnel 5.x instead
  Resolves: #301971
- Mark localized man pages with %%lang (patch by Ville Skyttä)
  Resolves: #322281

* Tue Aug 28 2007 Miloslav Trmač <mitr@redhat.com> - 4.20-3.nss
- Port to NSS

* Mon Dec  4 2006 Miloslav Trmac <mitr@redhat.com> - 4.20-2
- Update BuildRequires for the separate tcp_wrappers-devel package

* Thu Nov 30 2006 Miloslav Trmac <mitr@redhat.com> - 4.20-1
- Update to stunnel-4.20

* Sat Nov 11 2006 Miloslav Trmac <mitr@redhat.com> - 4.19-1
- Update to stunnel-4.19

* Wed Oct 25 2006 Miloslav Trmac <mitr@redhat.com> - 4.18-1
- Update to stunnel-4.18
- Remove unused stunnel.cnf from the src.rpm
- Fix some rpmlint warnings

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 4.15-2
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.15-1.1
- rebuild

* Sat Mar 18 2006 Miloslav Trmac <mitr@redhat.com> - 4.15-1
- Update to stunnel-4.15

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.14-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.14-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Miloslav Trmac <mitr@redhat.com> - 4.14-3
- Use pthread threading to fix crash on x86_64 (#179236)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Miloslav Trmac <mitr@redhat.com> - 4.14-2
- Rebuild with newer openssl

* Thu Nov  3 2005 Miloslav Trmac <mitr@redhat.com> - 4.14-1
- Update to stunnel-4.14
- Override changed default pid file location, keep it in %%{_localstatedir}/run

* Sat Oct 22 2005 Miloslav Trmac <mitr@redhat.com> - 4.13-1
- Update to stunnel-4.13

* Fri Sep 30 2005 Miloslav Trmac <mitr@redhat.com> - 4.12-1
- Update to stunnel-4.12

* Thu Sep 22 2005 Miloslav Trmac <mitr@redhat.com> - 4.11-2
- Enable IPv6 (#169050, patch by Peter Bieringer)
- Don't ship another copy of man pages in HTML

* Tue Jul 12 2005 Miloslav Trmac <mitr@redhat.com> - 4.11-1
- Update to stunnel-4.11
- Fix int/size_t mismatches in stack_info ()
- Update Certificate-Creation for /etc/pki

* Wed Jun  1 2005 Miloslav Trmac <mitr@redhat.com> - 4.10-2
- Fix inetd mode
- Remove unnecessary Requires: and BuildRequires:
- Clean up the spec file

* Tue Apr 26 2005 Nalin Dahyabhai <nalin@redhat.com> 4.10-1
- update to 4.10

* Tue Apr 26 2005 Nalin Dahyabhai <nalin@redhat.com> 4.08-2
- add buildprereqs on libtool, util-linux; change textutils/fileutils dep to
  coreutils (#133961)

* Wed Mar 16 2005 Nalin Dahyabhai <nalin@redhat.com> 4.08-1
- update to 4.08
- build stunnel as a PIE binary

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
- clean up %%post script
- make stunnel.pem %%ghost %%config(noreplace)
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
