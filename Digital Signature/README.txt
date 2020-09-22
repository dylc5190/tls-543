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
