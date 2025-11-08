import os, uuid, random, re, time
import requests, json

def sxr_main():
    os.system("clear")
    print("\033[1;37m")
    print("\033[1;92m══════════════════════════════════════════════════")
    print("\033[1;96m          FACEBOOK COOKIE EXTRACTOR")
    print("\033[1;92m══════════════════════════════════════════════════\n")
    
    # Prompt for email/UID
    uid = input("\033[1;93m[?] ENTER YOUR UID/EMAIL: \033[1;97m")
    
    # Prompt for password
    pww = input("\033[1;93m[?] ENTER YOUR PASSWORD: \033[1;97m")
    
    print("\033[1;92m\n[*] Processing login...\n")
    
    amazon = ("E6653","E6633","E6853","E6833","F3111","F3111 F3113","F5122","F3111 F3113","SO-04H","F3212","F3311","F8331","SO-02J","G3116","G8232")
    ua = "Mozilla/5.0 (Linux; Android "+str(random.randint(4,13))+"; "+str(random.choice(amazon))+"; Windows 10 Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Kiwi Chrome/"+str(random.randint(84,106))+".0."+str(random.randint(4200,4900))+"."+str(random.randint(40,140))+" Mobile Safari/537.36"
    check(uid, pww, ua)

oks = []
cps = []

def check(uid, pww, ua):
    try:
        session = requests.Session()
        
        # Get login page to extract necessary tokens
        git_fb = session.get("https://m.facebook.com/login/", headers={'User-Agent': ua}).text
        
        # Extract required tokens
        lsd = re.search(r'name="lsd" value="(.*?)"', git_fb)
        jazoest = re.search(r'name="jazoest" value="(.*?)"', git_fb)
        m_ts = re.search(r'name="m_ts" value="(.*?)"', git_fb)
        li = re.search(r'name="li" value="(.*?)"', git_fb)
        
        # Prepare login data
        _data = {
            'lsd': lsd.group(1) if lsd else '',
            'jazoest': jazoest.group(1) if jazoest else '',
            'm_ts': m_ts.group(1) if m_ts else '',
            'li': li.group(1) if li else '',
            'try_number': '0',
            'unrecognized_tries': '0',
            'email': uid,
            'pass': pww,
            'login': 'Log In',
            'bi_xrwh': '0'
        }
        
        _header = {
            'authority': 'm.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://m.facebook.com',
            'referer': 'https://m.facebook.com/login/',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': ua
        }
        
        # Submit login
        url = 'https://m.facebook.com/login/device-based/regular/login/?refsrc=deprecated&lwv=100'
        sxr_respns = session.post(url, data=_data, headers=_header, allow_redirects=False)
        
        # Get cookies
        login_coki = session.cookies.get_dict()
        
        print('\033[1;92m══════════════════════════════════════════════════')
        
        if "c_user" in login_coki:
            print("\033[1;92m[✓] Login Successful!")
            print('\033[1;92m══════════════════════════════════════════════════')
            
            # Format cookie string
            coki = ";".join([f"{key}={value}" for key, value in login_coki.items()])
            
            print(f"\033[1;93m[USER ID]: {login_coki.get('c_user')}")
            print(f"\033[1;96m[COOKIE]:\n{coki}")
            print('\033[1;92m══════════════════════════════════════════════════')
            
            oks.append(uid)
            
            # Save cookie to file
            with open('cookies.txt', 'a') as f:
                f.write(f"{uid}|{pww}|{coki}\n")
                
        elif "checkpoint" in login_coki:
            print(f'\033[1;91m[×] Account Checkpoint')
            print(f'\033[1;93m[!] {uid} | {pww}')
            cps.append(uid)
            
        else:
            print(f'\033[1;91m[×] Login Failed')
            print(f'\033[1;93m[!] {uid} | {pww}')
            print(f'\033[1;90m[DEBUG] Cookies received: {list(login_coki.keys())}')
            
    except Exception as e:
        print(f'\033[1;91m[ERROR]: {str(e)}')

sxr_main()
