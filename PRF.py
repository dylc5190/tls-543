from Crypto.Hash import HMAC,MD5,SHA
import Crypto
import sys

def P_hash(secret,seed,out_len,digestmod):

  h=HMAC.new(secret,digestmod=digestmod)
  h.update(seed)
  hash = h.digest()
  
  output = ''
  A = hash
  while out_len > 0:
    h = HMAC.new(secret,digestmod=digestmod)
    h.update(A+seed)
    hash = h.digest()
    if len(hash) < out_len: adv = len(hash)
    else: adv = out_len
    output += hash[:adv]
    out_len -= adv
    h = HMAC.new(secret,digestmod=digestmod)
    h.update(A)
    A = h.digest();

  return output


def PRF10(secret,label,seed,out_len):

  secret_len = len(secret)
  half_secret_len = ( secret_len / 2 ) + ( secret_len % 2 );
  seed = label + seed
  seed_len = len(seed)
  md5_out = P_hash( secret[:half_secret_len], seed, out_len, Crypto.Hash.MD5)
  sha1_out = P_hash( secret[half_secret_len:], seed, out_len, Crypto.Hash.SHA)

  output = bytearray(out_len)
  for i,(x,y) in enumerate(zip(md5_out,sha1_out)):
      output[i] = chr(ord(x)^ord(y))

  return str(output)  
  
def PRF12(secret,label,seed,out_len):

  seed = label + seed
  sha256_out = P_hash( secret, seed, out_len, Crypto.Hash.SHA256)

  return sha256_out
  
def get_seed_for_master_secret(client_random,server_random):
    return client_random+server_random

def get_seed_for_key_expansion(client_random,server_random):
    return server_random+client_random

def get_label_for_master_secret():
    return "master secret"

def get_label_for_key_expansion():
    return "key expansion"
	
	
if __name__ == "__main__":
   ''' test code here '''
