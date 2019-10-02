#include <stdio.h>
#include <stdlib.h>
#ifdef WIN32
#include <winsock2.h>
#include <windows.h>
#else
#include <arpa/inet.h>
#endif
#include "hex.h"
#include "sha.h"
#include "digest.h"
#include "huge.h"
#include "ecdsa.h"
