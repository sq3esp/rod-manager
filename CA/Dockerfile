FROM python:3.11.4-slim-buster

WORKDIR /certs_private
COPY ./openssl.cnf /certs_private/openssl.cnf
RUN mkdir certs crl newcerts private csr
RUN chmod 700 private
RUN touch index.txt
RUN echo 1000 > serial
RUN openssl genrsa -aes256 -out private/ca.key.pem -passout pass:foobar 4096 
RUN chmod 400 private/ca.key.pem
RUN openssl req -passin pass:foobar -config /certs_private/openssl.cnf \
    -key private/ca.key.pem \
    -new -x509 -days 7300 -sha256 -extensions v3_ca \
    -out certs/ca.cert.pem -subj "/C=PL/ST=Wielkopolska/O=RodManager/CN=rodmanagermaster.pl"
RUN chmod 444 certs/ca.cert.pem
RUN openssl x509 -noout -text -in certs/ca.cert.pem
RUN openssl genpkey -algorithm RSA -out private/server.key.pem
RUN chmod 400 private/server.key.pem
RUN openssl req -config /certs_private/openssl.cnf -key private/server.key.pem -new -out csr/server.csr.pem \
    -subj "/C=PL/ST=Wielkopolska/O=RodManager/CN=rodmanager.pl" -extensions v3_ca
RUN openssl x509 -req -sha256 -passin pass:foobar -days 375 -in csr/server.csr.pem -CA certs/ca.cert.pem -CAkey \
    private/ca.key.pem -out certs/server.cert.pem -extfile /certs_private/openssl.cnf -CAcreateserial -extensions server_cert
RUN mkdir /certs
RUN cp private/server.key.pem /certs/server.key.pem
RUN cp certs/server.cert.pem /certs/server.cert.pem
RUN chmod 444 certs/server.cert.pem

