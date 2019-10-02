#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#ifdef WIN32
#include <winsock2.h>
#include <windows.h>
#else
#include <arpa/inet.h>
#endif
#include "ssl.h"
#include "md5.h"
#include "des.h"
#include "rc4.h"
