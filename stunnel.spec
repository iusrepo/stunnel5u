Summary: SSL-encrypting socket wrapper.
Name: stunnel
Version: 3.10
Release: 2
Copyright: GPL
Group: Applications/Internet
URL: http://stunnel.mirt.net/ 
Source0: ftp://stunnel.mirt.net/stunnel/stunnel-%{version}.tar.gz
Source1: stunnel.cnf
Source2: Certificate-Creation
Source3: sfinger.xinetd
Source4: pop3-redirect.xinetd
Patch0: stunnel-3.10-64bit.patch
Patch1: stunnel-3.9-hup.patch
Buildroot: %{_tmppath}/stunnel-root
BuildPrereq: openssl-devel, textutils, fileutils, /usr/share/dict/words
Prereq: openssl >= 0.9.5a, textutils, fileutils, /bin/mktemp, /sbin/ldconfig, /usr/share/dict/words, /bin/hostname, /usr/bin/id, /usr/bin/getent

%description
stunnel is a socket wrapper which can be used to give ordinary
applications SSL (secure sockets layer) support. For example, it
can be used in conjunction with a imapd to create a SSL secure IMAP
server.

%prep
%setup -q
%patch0 -p1 -b .64bit
%patch1 -p1 -b .hup
cp %{SOURCE2} .

%build
CFLAGS="-g -DNO_RC5 -DNO_IDEA $RPM_OPT_FLAGS"; export CFLAGS
%configure \
	--with-ssl=%{_prefix} \
	--with-pem-dir=%{_datadir}/ssl/certs \
	--with-cert-file=%{_datadir}/ssl/cert.pem

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
