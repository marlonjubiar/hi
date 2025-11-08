import os, time, sys, uuid, string, random, re
from os import system as sm
from sys import platform as pf
from time import sleep as sp
try:
    import requests, bs4, rich, httpx
    from rich import print as rp
    from rich.panel import Panel as pan
    from requests import get as gt
    from requests import post as pt
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    sm('python -m pip install requests bs4 rich httpx')

#colors
R="[bold red]"
G="[bold green]"
Y="[bold yellow]"
B="[bold blue]"
M="[bold magenta]"
P="[bold violet]"
C="[bold cyan]"
W="[bold white]"
r="\033[1;31m"
g="\033[1;32m"
y="\033[1;33m"
b="\033[1;34m"
m="\033[1;35m"
c="\033[1;36m"
w="\033[1;37m"

def randc():
    randcolor=random.choice([R,G,Y,B,M,P,C,W])
    return randcolor

def logo():
    rp(pan("""%s                     ######   ######
                    ##    ## ##    ##
                    ##       ##    
                    ##       ##    
                    ##       ##
                    ##       ##   ####
                    ##       ##    ##
                    ##    ## ##    ##
                     ######   ######"""%(randc()),title="%sCOOKIE GETTER"%(Y),subtitle="%sDEVELOP BY PABLO"%(R),border_style=f"bold purple"))

def clear():
    if pf in ['win32','win64']:
        sm('cls')
    else:
        sm('clear')
    logo()

def get_response(url):
    session = requests.Session()
    return session.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
    })

def datr(user, passw):
    session = requests.Session()
    headers = {
        'authority': 'm.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
    }

    try:
        login_url = 'https://m.facebook.com/login/device-based/regular/login/'
        response = session.get(login_url, headers=headers)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        lsd = soup.find('input', {'name': 'lsd'})['value']
        jazoest = soup.find('input', {'name': 'jazoest'})['value']

        login_data = {
            'lsd': lsd,
            'jazoest': jazoest,
            'email': user,
            'pass': passw,
            'login': 'Log In'
        }

        login_response = session.post(login_url, data=login_data, headers=headers)
        cookies = session.cookies.get_dict()

        if 'c_user' in cookies:
            clear()
            print(f"{g}Successfully logged in!")
            cookie_string = '; '.join([f"{k}={v}" for k, v in cookies.items()])
            print(f"{c}Cookie: {g}{cookie_string}")
        elif 'checkpoint' in cookies:
            clear()
            print(f"{r}Account is in checkpoint")
        else:
            clear()
            print(f"{r}Invalid credentials")

    except Exception as e:
        print(f"{r}Error occurred: {str(e)}")
    
    input(f"{g}Press Enter to continue...")
    main()

def cuser(user, passw):
    device_id = str(uuid.uuid4())
    adid = str(uuid.uuid4())
    family_device_id = str(uuid.uuid4())
    
    data = {
        'adid': adid,
        'format': 'json',
        'device_id': device_id,
        'email': user,
        'password': passw,
        'generate_session_cookies': '1',
        'credentials_type': 'password',
        'source': 'login',
        'error_detail_type': 'button_with_disabled',
        'meta_inf_fbmeta': '',
        'advertiser_id': adid,
        'currently_logged_in_userid': '0',
        'locale': 'en_US',
        'client_country_code': 'US',
        'method': 'auth.login',
        'fb_api_req_friendly_name': 'authenticate',
        'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
        'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',  # Updated access token
        'api_key': '882a8490361da98702bf97a021ddc14d'
    }

    headers = {
        'User-Agent': '[FBAN/FB4A;FBAV/396.1.0.28.104;FBBV/429650999;FBDM/{density=2.25,width=720,height=1452};FBLC/en_US;FBRV/437165341;FBCR/Carrier;FBMF/OPPO;FBBD/OPPO;FBPN/com.facebook.katana;FBDV/CPH1893;FBSV/10;FBOP/1;FBCA/arm64-v8a:;]',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'b-api.facebook.com',
        'X-FB-Net-HNI': str(random.randint(20000, 40000)),
        'X-FB-SIM-HNI': str(random.randint(20000, 40000)),
        'Authorization': 'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32',  # Added authorization header
        'X-FB-Connection-Type': 'WIFI',
        'X-Tigon-Is-Retry': 'False',
        'x-fb-session-id': 'nid=jiZ+yNNBgbwC;pid=Main;tid=132;nc=1;fc=0;bc=0;cid=d29d67d37eca387482a8a5b740f84f62',
        'x-fb-device-group': '5120',
        'X-FB-Friendly-Name': 'authenticate',
        'X-FB-Request-Analytics-Tags': 'graphservice',
        'X-FB-HTTP-Engine': 'Liger',
        'X-FB-Client-IP': 'True',
        'X-FB-Server-Cluster': 'True',
        'x-fb-connection-token': 'd29d67d37eca387482a8a5b740f84f62'
    }

    try:
        response = httpx.post(
            'https://b-api.facebook.com/method/auth.login',  # Updated API endpoint
            data=data,
            headers=headers,
            timeout=30
        ).json()

        if 'access_token' in response:
            clear()
            print(f"{g}Login successful!")
            cookie_string = "sb=" + ''.join(random.choices(string.ascii_letters + string.digits + '_', k=24)) + "; "
            if 'session_cookies' in response:
                cookie_string += ';'.join([f"{cookie['name']}={cookie['value']}" for cookie in response['session_cookies']])
            print(f"{c}Cookie: {g}{cookie_string}")
            print(f"{c}Access Token: {g}{response.get('access_token', '')}")
        elif 'error_msg' in response:
            clear()
            print(f"{r}Login failed: {response['error_msg']}")
        else:
            clear()
            print(f"{r}Login failed or checkpoint required")
            print(response)
    
    except Exception as e:
        print(f"{r}Error occurred: {str(e)}")
    
    input(f"\n{c}Press Enter to continue...")
    main()


def main():
    clear()
    try:
        user = input(f"{c}(USER ID/EMAIL):~ ")
        passw = input(f"{c}(PASSWORD):~ ")
    except (KeyboardInterrupt, EOFError):
        print(f"{r}\nOperation cancelled by user")
        sys.exit(1)

    clear()
    rp(pan(f"{Y}[{C}1{Y}]{G} COOKIE 1(datr, fr, xs)\n{Y}[{C}2{Y}]{G} COOKIE 2(c_user w/ token)\n{Y}[{C}3{Y}]{R} EXIT",
           border_style="bold purple"))
    
    try:
        select = int(input(f"{c}Choose Number: {y}"))
        if select not in [1, 2, 3]:
            raise ValueError
    except ValueError:
        print(f"{r}Please enter a valid number (1-3)")
        sp(2)
        return main()

    if select == 1:
        datr(user, passw)
    elif select == 2:
        cuser(user, passw)
    else:
        sys.exit(f"{r}QUITTING")

if __name__ == "__main__":
    main()
