import sys
import socket
import struct

sites = ["Google.com",
"Youtube.com",
"Facebook.com",
"Baidu.com",
"Yahoo.com",
"Wikipedia.org",
"Amazon.com",
"Google.co.in",
"Qq.com",
"Twitter.com",
"Live.com",
"Taobao.com",
"Vk.com",
"Google.co.jp",
"Instagram.com",
"Weibo.com",
"Linkedin.com",
"Sina.com.cn",
"Yahoo.co.jp",
"Yandex.ru",
"Hao123.com",
"Bing.com",
"360.cn",
"Sohu.com",
"Msn.com",
"Google.de",
"Reddit.com",
"Google.com.br",
"Tmall.com",
"Google.co.uk",
"Onclickads.net",
"Google.fr",
"Ebay.com",
"T.co",
"Mail.ru",
"Google.it",
"Wordpress.com",
"Apple.com",
"Microsoft.com",
"Ok.ru",
"Amazon.co.jp",
"Netflix.com",
"Pinterest.com",
"Tumblr.com",
"Google.es",
"Blogspot.com",
"Blogger.com",
"Stackoverflow.com",
"Aliexpress.com"]


def parse_tls():
    with open('1.bin','rb') as f:
      buf = f.read()
      i = 0
      while i < len(buf):
        ctype, = struct.unpack(">B",buf[i:i+1])
        version, = struct.unpack(">H",buf[i+1:i+3])
        clength, = struct.unpack(">H",buf[i+3:i+5])
        print '{0}, {1}, {2}'.format(ctype,version,clength)
        i+=5
        if ctype != 22: # handshake
           i+=clength
           continue
        while clength:
          htype, = struct.unpack(">I",buf[i:i+4])
          hlength = htype & 0xffffff
          htype = (htype & 0xff000000) >> 24
          print '{0}, {1}'.format(htype,hlength)
          if htype== 12: #server key exchange
             prime_len, =struct.unpack(">H", buf[i+4:i+6])
             prime = buf[i+6:i+6+prime_len]
             print "prime({0}):{1}".format(prime_len,prime.encode('hex'))
             g_len_pos = i+6+prime_len
             g_len, =struct.unpack(">H", buf[g_len_pos:g_len_pos+2])
             g = buf[g_len_pos+2:g_len_pos+2+g_len]
             print "generator({0}):{1}".format(g_len,g.encode('hex'))
          clength -= (4+hlength)
          i+=(4+hlength)
    
def dump_dh_params(host):
    clientHello = '16030100d4010000d00303f1e522350d6d6ddc40affa96369a380c432abb6b5906f59b45434c5f0f395c8b00007a00a3009f006b006a003900380088008700a7006d003a008900a2009e0067004000330032009a00990045004400a6006c0034009b0046001800160013001b00150012001a001400110019001700a500a100690068003700360086008500a400a0003f003e0031003000980097004300420010000d000f000c00ff0100002d00230000000d0020001e060106020603050105020503040104020403030103020303020102020203000f000101'.decode('hex')
    PORT = 443
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
      s.connect((host, PORT))
      s.sendall(clientHello)
      with open("1.bin","wb") as f:
        data = s.recv(1024)
        while data:
          f.write(data)
          data = s.recv(1024)
          #print "recv ", len(data)
        s.close()
    except:
      pass

#host = sys.argv[1]
for host in sites:
    print host
    dump_dh_params(host)
    parse_tls()
