#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#ifdef WIN32
#include <windows.h>
#else
#include <unistd.h>
#endif
#include "base64.h"
#include "asn1.h"
