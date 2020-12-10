In the following steps, we'll use issuer's public key to verify the digital signature of a certificate.

1. Find the packet that contains certificates in cert.cap.
2. Export "signedCertificate" of the first certificate to the file xyz.cer.
   This is the certificate to be signed by the issuer.
3. Export "encrypted" parts under Certificate > algorithmIdentifier to the file xyz.sig.
   This is the digital signature (SHA256) of the certificate in step 2 and is encrypted (signed) by issuer's private key.
4. Export the second certificate to the file issuer.cer.
5. Export subjectPublicKeyInfo under Certificate > signedCertificate to the file issuer.pub.
6. Use either issuer's certificate (step 4) or public key (step 5) to verify the signature (step 3).
   a. openssl rsautl -keyform DER -inkey issuer.cer -certin -in xyz.sig -asn1parse
   b. openssl rsautl -keyform DER -inkey issuer.pub -pubin -in xyz.sig -asn1parse
   Output:
       0:d=0  hl=2 l=  49 cons: SEQUENCE
       2:d=1  hl=2 l=  13 cons:  SEQUENCE
       4:d=2  hl=2 l=   9 prim:   OBJECT            :sha256
      15:d=2  hl=2 l=   0 prim:   NULL
      17:d=1  hl=2 l=  32 prim:  OCTET STRING
         0000 - eb 5d aa 87 a5 ab c5 8c-f4 b8 9e c0 f3 88 fb 97   .]..............
         0010 - a3 59 fa 70 9e e6 00 29-a8 56 75 b1 73 ad 0e e2   .Y.p...).Vu.s...
7. Compute SHA256 of the certificate (step 2) by running "sha256sum xyz.cer"
   eb5daa87a5abc58cf4b89ec0f388fb97a359fa709ee60029a85675b173ad0ee2  xyz.cer

The values are the same.

In this scenario, we download the certificates (host and its issuer's) from a website, medium.com in this example, and extract the public key and the signature for verification.
Thanks to https://medium.com/@ebuschini/a-journey-into-verifying-signatures-on-x-509-certificates-168a5bafaa14
# Suppose we've downloaded medium-com.pem and medium-com-issuer.pem
$ openssl x509 -in medium-com-issuer.pem -noout -pubkey > medium-com-issuer.pub
$ openssl x509 -in medium-com.pem -outform der -out medium-com.der
# Considering 
# Certificate  ::=  SEQUENCE  {
#        tbsCertificate       TBSCertificate,
#        signatureAlgorithm   AlgorithmIdentifier,
#        signatureValue       BIT STRING  }
# we can extract signature part from specific offset. Although we use pem as input, the offset is for der.
# The signature part has 257 bytes. The first byte is used for padding and here it is 0x00 so we skip it.
$ openssl asn1parse -in medium-com.pem | grep d=[01]
    0:d=0  hl=4 l=1850 cons: SEQUENCE          
    4:d=1  hl=4 l=1570 cons: SEQUENCE          
 1578:d=1  hl=2 l=  13 cons: SEQUENCE          
 1593:d=1  hl=4 l= 257 prim: BIT STRING        
$ cat medium-com.der | dd skip=$((4+4+1570+2+13+4+1)) bs=1 > medium-com.sig
256+0 records in
256+0 records out
256 bytes copied, 0.00154862 s, 165 kB/s
# Extract tbsCertificate to compute sha256 for comparison
$ cat medium-com.der | dd skip=4 count=$((4+1570)) bs=1 > medium-com.tbs
1574+0 records in
1574+0 records out
1574 bytes (1.6 kB, 1.5 KiB) copied, 0.00321419 s, 490 kB/s
$ openssl rsautl -verify -pubin -inkey medium-com-issuer.pub -in medium-com.sig | openssl asn1parse -inform der
    0:d=0  hl=2 l=  49 cons: SEQUENCE          
    2:d=1  hl=2 l=  13 cons: SEQUENCE          
    4:d=2  hl=2 l=   9 prim: OBJECT            :sha256
   15:d=2  hl=2 l=   0 prim: NULL              
   17:d=1  hl=2 l=  32 prim: OCTET STRING      [HEX DUMP]:60A4A38ED132C1E38115298069DCCB27CBDD29989D096B902F4F87C6E4054290
$ sha256sum medium-com.tbs 
60a4a38ed132c1e38115298069dccb27cbdd29989d096b902f4f87c6e4054290  medium-com.tbs

The sha256 values are the same.
