import random
import socket

def primitive_root(b,n):
    for i in xrange(1,n):
        print '{0}^{1} % {2} = {3}'.format(b,i,n,pow(b,i,n))

def dh_key_exchange(g,p,a,b):
     
    Ya = pow(g,a,p)
    print "server holds a({0}) as secret".format(a)
    print "server gives g({0}), p({1}) and Ya({2})".format(g,p,Ya)

    Yb = pow(g,b,p)
    print "client holds b({0}) as secret".format(b)
    print "client responds Yb({0})".format(Yb) 
    print "client computes Ya^b %p = {0} as shared key".format(pow(Ya,b,p))
    print "server computes Yb^a %p = {0} as shared key".format(pow(Yb,a,p))

    print "the man in the middle wants to compute i such that g^i%p = Ya"
    for i in xrange(1,p):
        Y = pow(g,i,p)
        if Y == Ya:
           print "==> g^{0} %p = {1} ---- Bingo!".format(i,Y)
        else:
           print "==> g^{0} %p = {1}".format(i,Y)

def mypow(x, n, P):
    #double and add?
    result = 1
    while n:
      if n % 2:
        result = (result * x) % P
        n = n - 1
      x = (x * x) % P
      n = n / 2
    return result
     
def brute_force_dh():
    G = long(2)
    P = long(0x96c99b60c4f823707b47a848472345230c5b25103dc37412a701833e8ff5c567a53a41d0b37b10f0060d50f4131c57cf1fd11b6a6cb958f36b1e7d878a4c4bc7)
     
    a = random.getrandbits(512)
    #A = (G ** a) % P # G^a mod P
    Y = pow(G, a, P) #c.f. pow(G, a) which is going to be much, much slower
                     #mypow(G, a, P) same as pow. just to see how it works.
    print Y
    i=long(1)
    while i < a:
        Yi = pow(G, i, P)
        if Yi == Y: break
        i += 1
        if i%100000 == 0: print i


#brute_force_dh()

#dh_key_exchange(g=2,p=11,a=8,b=6)
#dh_key_exchange(g=2,p=10000,a=711,b=445)
#dh_key_exchange(g=3,p=10,a=20,b=15)
#dh_key_exchange(g=2,p=10,a=20,b=15)
dh_key_exchange(g=101,p=23310837,a=17364857,b=6783475)
exit()

#http://www.oxfordmathcenter.com/drupal7/node/384
#3 is not primitive root of 26 but 7 is
primitive_root(3,26)
primitive_root(7,26)
#4 is not primitive root of 19 but 3 is
primitive_root(4,19)
primitive_root(3,19)