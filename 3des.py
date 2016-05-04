from Crypto.Cipher import DES3
import PRF

client_random = '5722c68e00000000000000000000000000000000000000000000000000000000'.decode('hex')
server_random = '00be8a58ef4482d3dc36f2b5b4b2fdd322c08262ae2455c1992549e0e8497ff6'.decode('hex')
#Usually this is not available unless you have private key. I knew this because the client I used is written by myself, not a browser.
premaster = '030102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f'.decode('hex')

seed = PRF.get_seed_for_master_secret(client_random,server_random)
label = PRF.get_label_for_master_secret()
secret = premaster
master_key = PRF.PRF10(secret,label,seed,48) #master key is always 48 bytes. 
print "master: " + master_key.encode('hex')

seed = PRF.get_seed_for_key_expansion(client_random,server_random)
label = PRF.get_label_for_key_expansion()
secret = master_key
key_block = PRF.PRF10(secret,label,seed,104) #length depends on cipher suite. 104 is for 3DES.
#I only need "sender" part now
MAC = key_block[0:20]
SESSION_KEY = key_block[40:64]
IV = key_block[88:96]
print "key: " + SESSION_KEY.encode('hex')
print "IV: " + IV.encode('hex')

#12th packet (try view the pcap without premaster file in Wireshark)
finished = 'bd568d8a12a77cf04c23c2ea61d464634f9f70266601fdad20df67d1665235cd9bbe62eecad55adf'
cipher = DES3.new(SESSION_KEY,DES3.MODE_CBC,IV=IV)
finished_dec = cipher.decrypt(finished.decode('hex'))
print "verifiy data: " + finished_dec.encode('hex')
