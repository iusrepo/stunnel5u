To convert an existing stunnel set up to NSS, at minimum it is necessary to:
- create a NSS database directory, $SSL_DIR
  $ certutil -d $SSL_DIR -N
- import server and CA certificates:
  $ certutil -d $SSL_DIR -A -n server_cert_nickname -i server_cert.pem
- import server private key:
  $ openssl pkcs12 -export -in server_key.pem -out server_key.pfx
  $ pk12util -d $SSL_DIR -i server_key.pfx
- modify stunnel.conf to use "server_cert_nickname" instead of path to
  "server_cert.pem" in "cert"
- when starting stunnel, make sure $SSL_DIR is present in the
  environment
