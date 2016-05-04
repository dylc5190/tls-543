from OpenSSL.crypto import load_publickey, dump_publickey, FILETYPE_ASN1, FILETYPE_PEM
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Util import asn1
from Crypto.Cipher import DES3
from OpenSSL._util import (
     ffi as _ffi,
     lib as _lib)

import M2Crypto
import PRF

#dump from pyOpenSSL
client_random = '2abb666bdb5e6319ba5efb845c46f7b9d093bf0b38c7aa730730979a59faab01'.decode('hex')
server_random = 'ffc6a03c03be63ddf441d2d336d1813299d12f60307d5459c1cd0f3ea9f4d03c'.decode('hex')
#pyOpenSSL dumps master secret instead of premaster secret (same as browser's $SSLKEYLOGFILE and this is what Wireshark needs)
#master key 076ba8515c6ed860177d274f6378671f9e3215099b15dc39b3afe76a22fe3555ce12b36b213bd6695a18afc26c796787

#following data are in 6th packet
#subjectPublicKeyInfo of the certificate which is self-signed
key = '30820122300d06092a864886f70d01010105000382010f003082010a0282010100b12817aacae87f9f0774a9e189a0c61b036ae5a4b3947b6cf9dd78d5c603ef47409c2090c0e81879a0209498f90653880f0ede8173c9bc715fc184aabda992379cd73a5d10306a3971a83fe005ba00c2e28e48f46780fd42d3ebed1a84a7946953b171d8f984ce340e1bfde66248a2cbf71da5432898406be68f76e47a4ff4f7c1fa786631e1ae213402b5383de785164282a66cb0c860f2d476de8b2a504c03301d253d90942435c1f25bf5027670d0add7b1e39ffe14892e4b70989da24a7beb7e450a08375d6b33cc0831f4565b90c52e0f1cbc3f47c1542d2d76ac8145ee08effc975c0e2300ade32f212b68bfd7faad20595dc8b9d580d3946d6f628d930203010001'.decode('hex')
#encrypted hash of the certificate
encHash = '17b46b40bccd244e747b5bc18b7c2e29bcfb218a5b4811c20126cc61b7c1bb2c60b4d2c468ab4c3c77836636bde806c24beb130fc83aee27865dac062ca370557de3449c33db2b76a6270f0b94c650a22bd2978d0620ab227884c335d9272c715e5e6610c65640b3bdfe046ab7a6e83d6eef9571efabed1ca1400ab53593549b413a53ea95460cca29bd9079e3ffaabedbdc3fa728c3173c22c0721da7bc0f5e7c33c1849fe82f37813bf36dde834d3041b2265fcfda0108ea93d39e53e5279892ae88f5540c87c704bc0e808c4d7706d7e8f78839a29c53be2b1697d9e2761f4411b7374fea668c75f632e333e90e8712292085430780b2264f1764c372590f'.decode('hex')
#certificate to be singed (see signedCertificate field in Wireshark)
cert = '3082020c020900e30ccd03d2c268cc300d06092a864886f70d01010505003054310b3009060355040613025457310b300906035504080c025457310c300a06035504070c03545049310e300c060355040a0c055452454e44311a301806035504030c116e6369652e7472656e642e636f6d2e7477301e170d3136303231363037333631375a170d3137303231353037333631375a3054310b3009060355040613025457310b300906035504080c025457310c300a06035504070c03545049310e300c060355040a0c055452454e44311a301806035504030c116e6369652e7472656e642e636f6d2e747730820122300d06092a864886f70d01010105000382010f003082010a0282010100b12817aacae87f9f0774a9e189a0c61b036ae5a4b3947b6cf9dd78d5c603ef47409c2090c0e81879a0209498f90653880f0ede8173c9bc715fc184aabda992379cd73a5d10306a3971a83fe005ba00c2e28e48f46780fd42d3ebed1a84a7946953b171d8f984ce340e1bfde66248a2cbf71da5432898406be68f76e47a4ff4f7c1fa786631e1ae213402b5383de785164282a66cb0c860f2d476de8b2a504c03301d253d90942435c1f25bf5027670d0add7b1e39ffe14892e4b70989da24a7beb7e450a08375d6b33cc0831f4565b90c52e0f1cbc3f47c1542d2d76ac8145ee08effc975c0e2300ade32f212b68bfd7faad20595dc8b9d580d3946d6f628d930203010001'.decode('hex')
#calculate SHA1 of certificate for later comparison
print "SHA1: " + SHA.new(cert).hexdigest()

############################################################
#                                                          #
#    part 1                                                #
#                                                          #
#    decrypt signature. same as what rsa_pubkey.py does    #
#                                                          #
############################################################

pubkey = load_publickey(FILETYPE_ASN1,key)
f = open("pub.pem","wb+")
f.write(dump_publickey(FILETYPE_PEM, pubkey))
f.close()
print "Pubkey: " + str(pubkey.bits()) + " bits,",
rsa = _lib.EVP_PKEY_get1_RSA(pubkey._pkey)
print str(_lib.RSA_size(rsa)) + " bytes."

#Got problem with pyOpenSSL to decrypt so use M2Crypto instead
#result = _lib.RSA_public_decrypt(len(encHash),encHash,decHash,rsa,_lib.RSA_PKCS1_PADDING)
rsa = M2Crypto.RSA.load_pub_key('pub.pem')
decHash = rsa.public_decrypt(encHash,M2Crypto.RSA.no_padding)
print "PKCS #1 data of signature\n", decHash.encode('hex')
#see rfc 3447 9.2 EMSA-PKCS1-v1_5
nextZero = decHash[2:].find("\x00") + 2
decHash = decHash[nextZero+1:]					#asn.1 DER-encoded
#extract actual data in asn.1 using Crypto.Util.asn1
der = asn1.DerSequence()
der.decode(decHash)
#der[0] is OID
der_sig_in = asn1.DerObject()
der_sig_in.decode(der[1])
print "Decrypted SHA1: " + der_sig_in.payload.encode('hex')

############################################################
#                                                          #
#    part 2                                                #
#                                                          #
#    decrypt premaster. we can do this because we have     #
#    private key in hand                                   #
#                                                          #
############################################################

print
encPremaster = '2cbefb0b9661593ccd00fb74fe61df41cd583022a9e5eb445f76d437fec87ec0339deb8da94c9b9d16a818df8950287925d1b9d020451601ba4876cd1b656ecad70d1f810339468ecd1d38707041cf890458325b8fc582072ffdf0615bf15e33fbe2897e7dd1012bcfe69d11e96dd646cb23edc53126b7e9bf648362d38c102d4d9175341a4ac41b51ff8a1a1d690f094b40077af854021f4d0ff0e252dfa80bac8d71fc2b3eb8053b81685ed84da73b59e0903b3c2f32d1259747cbfab2195984addce75db8435b0ccd712ac4cbbec7eb06c19ceb73047cf567e524ec8e8d174291025c92292f702117c0c4c9c4d60ad5545e0227f55f7af1645faa20cdd6f3'.decode('hex')
rsa = M2Crypto.RSA.load_key('priv.key')
#the result should be the same as what openssl decrypts
# openssl rsautl -decrypt -inkey priv.key -in encPremaster.txt -out decPremaster.txt
# decPremaster.txt is '0303132d534bbf989874faa463ee5123391eab2da44f6ca6d43025d69cca617920558fac14a7da8eed46a7af827551eb'
decPremaster = rsa.private_decrypt(encPremaster,M2Crypto.RSA.no_padding)
print "PKCS #1 data of premaster:\n",decPremaster.encode('hex')
#see rfc 3447 7.2.2 RSAES-PKCS1-V1_5 step 3
nextZero = decPremaster[2:].find("\x00") + 2
decPremaster = decPremaster[nextZero+1:]
print "Decrypted premaster: " + decPremaster.encode('hex')

############################################################
#                                                          #
#    part 3                                                #
#                                                          #
#    decrypt verifiy data. same as what 3des.py does but   #
#    notice the PRF function used is different.            #
#                                                          #
############################################################

print
seed = PRF.get_seed_for_master_secret(client_random,server_random)
label = PRF.get_label_for_master_secret()
secret = decPremaster
master_key = PRF.PRF12(secret,label,seed,48) #master key is always 48 bytes. 
print "master: " + master_key.encode('hex')

seed = PRF.get_seed_for_key_expansion(client_random,server_random)
label = PRF.get_label_for_key_expansion()
secret = master_key
key_block = PRF.PRF12(secret,label,seed,104) #length depends on cipher suite. 104 is for 3DES.
#I only need "sender" part now
MAC = key_block[0:20]
SESSION_KEY = key_block[40:64]
IV = key_block[88:96]
print "key: " + SESSION_KEY.encode('hex')
print "IV: " + IV.encode('hex')

finished = '4f10a0347b552c614d9f446597a92a27aa499b7118faa6335fde3f22d7f4b944d7a7713facb1d9768b6a93c4b5c3af2a'
cipher = DES3.new(SESSION_KEY,DES3.MODE_CBC,IV=IV)
finished_dec = cipher.decrypt(finished.decode('hex'))
print "verifiy data: " + finished_dec.encode('hex')
