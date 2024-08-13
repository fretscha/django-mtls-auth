#!/bin/bash 

rm -f *.csr *.key *.crt *.srl *.p12 


# Create CA Cert
CA_NAME=DummyCA
openssl genrsa -out $CA_NAME.key 4096
openssl rsa -in $CA_NAME.key -noout -check
openssl req -new -key $CA_NAME.key -out $CA_NAME.csr -subj "/CN=$CA_NAME Root CA/C=CH/ST=Bern/L=Bern/O=MyOrg"
openssl x509 -req -days 3650 -in $CA_NAME.csr -signkey $CA_NAME.key -out $CA_NAME.crt -extfile ca.ext
# openssl x509 -in $CA_NAME.crt -text -noout | grep -A10 "X509v3 extensions"



# Create Server Cert
MY_SERVER=localhost
openssl req -new -nodes -out $MY_SERVER.csr -newkey rsa:4096 -keyout $MY_SERVER.key -subj '/CN=localhost.local/C=CH/ST=Bern/L=Bern/O=MyOrg'
# create a v3 ext file for SAN properties

openssl x509 -req -days 730 -in $MY_SERVER.csr -CA $CA_NAME.crt -CAkey $CA_NAME.key -CAcreateserial -out $MY_SERVER.crt -sha256 -extfile server.ext


# Create Client Cert
MY_CLIENT=client
openssl req -new -nodes -out $MY_CLIENT.csr -newkey rsa:4096 -keyout $MY_CLIENT.key -subj '/O=MyOrg,/L=Bern,/ST=Bern,/C=CH,/GN=test,/SN=client,/E=test.client@client.tld,/CN=Test Client (user2845)'

openssl x509 -req -days 730 -in $MY_CLIENT.csr -CA $CA_NAME.crt -CAkey $CA_NAME.key -CAcreateserial -out $MY_CLIENT.crt -sha256 -extfile client.ext



# create pkcs12 file for client
echo "Creating PKCS12 file for client"

cat $MY_CLIENT.crt $CA_NAME.crt > $MY_CLIENT-fullchain.crt

openssl pkcs12 -export -legacy -inkey $MY_CLIENT.key  -in $MY_CLIENT-fullchain.crt  -out $MY_CLIENT.p12 -name "MyOrg Test Client Certificate" 




