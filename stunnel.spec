Summary: SSL-encrypting socket wrapper.
Name: stunnel
Version: 3.8
Release: 4
Copyright: GPL
Group: Applications/Internet
Source0: http://mike.daewoo.com.pl/computer/stunnel/stunnel-%{version}.tar.gz
Source1: stunnel.cnf
Source2: Certificate-Creation
Source3: sfinger.xinetd
Patch0: stunnel-3.8-redhat.patch
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
%patch0 -p1 -b .redhat
cp %{SOURCE2} .

%build
CFLAGS="$RPM_OPT_FLAGS -DNO_RC5 -DNO_IDEA"; export CFLAGS
%configure --with-ssl=%{_datadir}/ssl

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
make

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall} \
	ssldir=$RPM_BUILD_ROOT/%{_datadir}/ssl \
	man8dir=$RPM_BUILD_ROOT%{_mandir}/man8 \
	piddir=$RPM_BUILD_ROOT/%{_var}/run
install -m644 stunnel.cnf $RPM_BUILD_ROOT/%{_datadir}/ssl/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc BUGS COPY* FAQ HISTORY PORTS README TODO INSTALL stunnel.html *.txt
%doc $RPM_SOURCE_DIR/Certificate-Creation $RPM_SOURCE_DIR/sfinger.xinetd
%ghost %config(noreplace,missingok) %{_datadir}/ssl/certs/stunnel.pem
%{_libdir}/stunnel.so*
%{_mandir}/man8/stunnel.8*
%{_sbindir}/stunnel

%changelog
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
