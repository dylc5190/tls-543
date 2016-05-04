Description
===========
 Various, and not well-organized, stuff about TLS.

Environment Setup
=================
  - Install pyOpenSSL
    o Windows
	  pip install pyOpenSSL
    o Ubuntu
	  apt-get install libffi-dev
	  pip install pyOpenSSL
  - pip install cryptography
  - Install pycrypto
    o Windows x86
	  run pycrypto-2.6.win32-py2.7.exe
  - Install M2Crypto
    o Windows x86
      unzip M2Crypto-0.21.1-openssl-1.0.1e-py2.7-win32.zip
      copy M2Crypto %PYTHON_HOME%\Lib\site-packages
      copy *.dll %PYTHON_HOME%\Lib\site-packages\M2Crypto
      copy __m2crypto.* %PYTHON_HOME%\Lib\site-packages\M2Crypto
	o Windows x64
	  not succeed yet
	o Ubuntu
	  apt-get insatll swig

Files
=====
  - python scripts for SSL
    pyopenssl_client.py
	pyssl_client.py
  - examples of decryption
    3des.py
    3des.cap
    rsa_privkey.py
	rsa_privkey.cap
	rsa_pubkey.py
	rsa_pubkey.cap
	PRF.py
  - key exchange
    tls_dhe_rsa.cap
	tls_ecdhe.cap
	tls_rsa.cap
  