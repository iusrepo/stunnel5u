Summary: An SSL-encrypting socket wrapper.
Name: stunnel
Version: 3.17
Release: 1
License: GPL
Group: Applications/Internet
URL: http://stunnel.mirt.net/ 
Source0: ftp://stunnel.mirt.net/stunnel/stunnel-%{version}.tar.gz
Source1: stunnel.cnf
Source2: Certificate-Creation
Source3: sfinger.xinetd
Source4: pop3-redirect.xinetd
Buildroot: %{_tmppath}/stunnel-root
BuildPrereq: openssl-devel, perl, textutils, fileutils, /usr/share/dict/words, tcp_wrappers
Prereq: textutils, fileutils, /bin/mktemp, /sbin/ldconfig, /usr/share/dict/words, /bin/hostname, /usr/bin/id, /usr/bin/getent
Requires: make

%description
Stunnel is a socket wrapper which can provide SSL (Secure Sockets
Layer) support to ordinary applications. For example, it can be used
in conjunction with imapd to create an SSL secure IMAP server.

%prep
%setup -q

%build
%configure \
	--with-ssl=%{_prefix} \
	--with-pem-dir=%{_datadir}/ssl/certs \
	--with-cert-file=%{_datadir}/ssl/cert.pem \
	--with-tcp-wrappers

# We have to create a certificate before the makefile asks us to.
rm -f stunnel.pem stunnel.pem.1 stunnel.pem.2
(echo US
 echo .
 echo .
 echo .
 echo .
 echo .
 echo .
 echo .) | openssl req -newkey rsa:1024 -nodes -keyout stunnel.pem.1 -x509 -days 365 -out stunnel.pem.2
cat stunnel.pem.1 >  stunnel.pem
echo ""           >> stunnel.pem
cat stunnel.pem.2 >> stunnel.pem
make piddir=/var/run/

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall} \
	ssldir=$RPM_BUILD_ROOT/%{_datadir}/ssl \
	man8dir=$RPM_BUILD_ROOT%{_mandir}/man8 \
	piddir=$RPM_BUILD_ROOT/%{_var}/run \
	PEM_DIR=$RPM_BUILD_ROOT/%{_datadir}/ssl/certs
install -m644 stunnel.cnf $RPM_BUILD_ROOT/%{_datadir}/ssl

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc BUGS COPY* FAQ HISTORY PORTS README TODO stunnel.html *.txt
%doc $RPM_SOURCE_DIR/Certificate-Creation
%doc $RPM_SOURCE_DIR/sfinger.xinetd $RPM_SOURCE_DIR/pop3-redirect.xinetd
%ghost %config(noreplace,missingok) %{_datadir}/ssl/certs/stunnel.pem
%{_libdir}/stunnel.so*
%{_mandir}/man8/stunnel.8*
%{_sbindir}/stunnel

%changelog
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
