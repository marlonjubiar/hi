import sys
import os
os.system('clear')
import requests
import threading
import json
from time import strftime
from pystyle import Colorate, Colors, Write, Add, Center

__ZALO__ = 'https://zalo.me/g/apmxom704'
__ADMIN__ = 'D One'
__SHOP__ = 't.me/DeveloperTiktok016'
__VERSION__ = '1.0'
__NHV__ = '\033[1;91m[\033[1;92m●\033[1;91m]\033[1;97m ➻❥'  

def banner():
    print(f''' 
\033[1;34m╔═════════════════════════════════════════════════════════════════|               
██████╗      ██████╗ ███╗   ██╗███████╗
██╔══██╗    ██╔═══██╗████╗  ██║██╔════╝
██║  ██║    ██║   ██║██╔██╗ ██║█████╗  
██║  ██║    ██║   ██║██║╚██╗██║██╔══╝  
██████╔╝    ╚██████╔╝██║ ╚████║███████╗
╚═════╝      ╚═════╝ ╚═╝  ╚═══╝╚══════╝ v1.0
\033[1;34m╠═════════════════════════════════════════════════════════════════|
\033[1;32m║➢ Author       :Cyraxmod D One                                   
\033[1;36m║➢ Acleda       :0884152630                  
\033[1;31m║➣ Link Group   :https://t.me/ShareToolBuffViewTikTok      
\033[1;33m║➣ Buy Tool VIP :https://t.me/DeveloperTiktok016                    
\033[1;34m╚═════════════════════════════════════════════════════════════════|
          ''')
    t = Colorate.Horizontal(Colors.white_to_black, "- - - - - - - - - - - - - - - - - - - - - - - - -")
    print(t)

def clear():
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')

gome_token = []

def get_token(input_file):
    for cookie in input_file:
        header_ = {
            'authority': 'business.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'referer': 'https://www.facebook.com/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
        }
        try:
            home_business = requests.get('https://business.facebook.com/content_management', headers=header_).text
            token = home_business.split('EAAG')[1].split('","')[0]
            cookie_token = f'{cookie}|EAAG{token}'
            gome_token.append(cookie_token)
        except:
            pass
    return gome_token

def share(tach, id_share):
    cookie = tach.split('|')[0]
    token = tach.split('|')[1]
    he = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'connection': 'keep-alive',
        'content-length': '0',
        'cookie': cookie,
        'host': 'graph.facebook.com'
    }
    try:
        res = requests.post(f'https://graph.facebook.com/me/feed?link=https://m.facebook.com/{id_share}&published=0&access_token={token}', headers=he).json()
    except:
        pass
    
def main_share():
    clear()
    banner()
    
    # Get cookie file with error handling
    while True:
        cookie_file = input("\033[1;31m[\033[1;37m=.=\033[1;31m] \033[1;37m=> \033[1m\033[38;5;51mName File Cookies: \033[1;35m").strip()
        
        # Auto-detect if user just typed filename without path
        if not '/' in cookie_file:
            # Try common Termux storage locations
            possible_paths = [
                f'/storage/emulated/0/{cookie_file}',
                f'/sdcard/{cookie_file}',
                f'/data/data/com.termux/files/home/{cookie_file}',
                cookie_file
            ]
            
            found = False
            for path in possible_paths:
                if os.path.exists(path):
                    cookie_file = path
                    found = True
                    print(f"\033[1;32m[FOUND] Using file: {cookie_file}\033[0m")
                    break
            
            if not found:
                print(f"\033[1;31m[ERROR] File '{cookie_file}' not found in any location!\033[0m")
                print(f"\033[1;33m[SEARCHED IN]:\033[0m")
                for path in possible_paths:
                    print(f"  • {path}")
                retry = input("\033[1;36mTry again? (y/n): \033[0m").lower()
                if retry != 'y':
                    sys.exit()
                continue
        
        # Check if full path exists
        if os.path.exists(cookie_file):
            try:
                with open(cookie_file, 'r') as f:
                    input_file = f.read().strip().split('\n')
                    input_file = [cookie.strip() for cookie in input_file if cookie.strip()]
                break
            except Exception as e:
                print(f"\033[1;31m[ERROR] Cannot read file: {e}\033[0m")
                retry = input("\033[1;36mTry again? (y/n): \033[0m").lower()
                if retry != 'y':
                    sys.exit()
        else:
            print(f"\033[1;31m[ERROR] File '{cookie_file}' not found!\033[0m")
            print(f"\033[1;33m[TIP] Use full path like: /storage/emulated/0/cookies.txt\033[0m")
            retry = input("\033[1;36mTry again? (y/n): \033[0m").lower()
            if retry != 'y':
                sys.exit()
    
    id_share = input("\033[1;31m[\033[1;37m=.=\033[1;31m] \033[1;37m=> \033[1m\033[38;5;51mLink ID Can Share: \033[1;35m")
    total_share = int(input("\033[1;31m[\033[1;37m=.=\033[1;31m] \033[1;37m=> \033[1m\033[38;5;51mNumber of Share Bot: \033[1;35m"))
    
    print(f'\033[1;33m[INFO] Processing {len(input_file)} cookies...\033[0m')
    all = get_token(input_file)
    total_live = len(all)
    print(f'\033[1;31m────────────────────────────────────────────────────────────')
    print(f'\033[1;32m[SUCCESS] Found {total_live} valid tokens!\033[0m')
    
    if total_live == 0:
        print(f'\033[1;31m[ERROR] No valid tokens found! Check your cookies.\033[0m')
        sys.exit()
    stt = 0
    while True:
        for tach in all:
            stt = stt + 1
            threa = threading.Thread(target=share, args=(tach, id_share))
            threa.start()
            print(f'\033[1;91m[\033[1;33m{stt}\033[1;91m]\033[1;31m ❥ \033[1;95mSHARE\033[1;31m ❥\033[1;36m Success\033[1;31m ❥ ID ❥\033[1;31m\033[1;93m {id_share} \033[1;31m❥ \n', end='\r')
        if stt == total_share:
            break
    gome_token.clear()
    input('\033[38;5;245m[\033[1;32mSUCCESS\033[38;5;245m] \033[1;32mBot Share Complete |  Press [Enter] to run again \033[0m\033[0m')

while True:
    try:
        main_share()
    except KeyboardInterrupt:
        print('\n\033[38;5;245m[\033[38;5;9m!\033[38;5;245m] \033[38;5;9mDo not forget to Join Group Channel ^^\033[0m')
        sys.exit()
