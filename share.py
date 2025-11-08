# zinkx.py - Enhanced Facebook Share Bot
import asyncio
import aiohttp
import re
import sys
import os
import time
import json
import requests
from rich.console import Console
from rich.panel import Panel
from rich import print as printf
from datetime import datetime
import pytz
from concurrent.futures import ThreadPoolExecutor
import signal

console = Console()

API_URL = "https://zinktoolsx.onrender.com"
TOKEN_FILE = "Zink/token.json"

CONFIGURATION = {
    'cookies': [],
    'cookie_uids': [],
    'access_tokens': [],
    'post': None,
    'user_token': None,
    'username': None,
    'user_id': None,
    'total_shares': 0,
    'member_since': None
}

SUKSES, GAGAL, BLOCKED_COOKIES = [], [], []
START_TIME = None
END_TIME = None
RUNNING = True

def signal_handler(sig, frame):
    global RUNNING
    RUNNING = False
    printf("\n[bold yellow]   ──> Gracefully stopping... Please wait...[/bold yellow]")

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

class AUTH:
    def __init__(self) -> None:
        if not os.path.exists('Zink'):
            os.makedirs('Zink')

    def LOAD_TOKEN(self) -> bool:
        try:
            if os.path.exists(TOKEN_FILE):
                with open(TOKEN_FILE, 'r') as f:
                    data = json.load(f)
                    CONFIGURATION['user_token'] = data.get('token')
                    CONFIGURATION['username'] = data.get('username')
                    return True
        except:
            pass
        return False

    def SAVE_TOKEN(self, token: str, username: str) -> None:
        try:
            with open(TOKEN_FILE, 'w') as f:
                json.dump({'token': token, 'username': username}, f)
        except:
            pass

    def DELETE_TOKEN(self) -> None:
        try:
            if os.path.exists(TOKEN_FILE):
                os.remove(TOKEN_FILE)
            CONFIGURATION['user_token'] = None
            CONFIGURATION['username'] = None
            CONFIGURATION['total_shares'] = 0
            CONFIGURATION['member_since'] = None
        except:
            pass

    def GET_PROFILE(self) -> bool:
        try:
            printf(f"[bold bright_white]   ──>[bold yellow] LOADING PROFILE...", end='\r')
            response = requests.get(
                f"{API_URL}/api/profile",
                headers={'Authorization': f'Bearer {CONFIGURATION["user_token"]}'},
                timeout=10
            )
            data = response.json()
            if data.get('success'):
                user = data['user']
                CONFIGURATION['username'] = user['username']
                CONFIGURATION['total_shares'] = user.get('totalShares', 0)
                CONFIGURATION['member_since'] = user.get('createdAt', 'Unknown')
                printf(f"[bold bright_white]   ──>[bold green] PROFILE LOADED!", end='\r')
                return True
            else:
                printf(f"[bold bright_white]   ──>[bold red] {data.get('message', 'FAILED!')}", end='\r')
                time.sleep(1)
                self.DELETE_TOKEN()
                return False
        except:
            printf(f"[bold bright_white]   ──>[bold red] CONNECTION ERROR!", end='\r')
            time.sleep(1)
            return False

    def INPUT_TOKEN(self) -> bool:
        try:
            printf(Panel(f"[bold white]To use this tool, you need an access token.\n\n[bold cyan]Get your token at:\n[bold yellow]{API_URL}\n\n[bold white]1. Login/Signup\n2. Copy your token from profile", width=56, style="bold bright_white", title="[bold bright_white][ Token Required ]", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
            token = console.input("[bold bright_white]   ╰─> ").strip()
            if not token:
                printf(Panel(f"[bold red]Token cannot be empty!", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
                return False
            printf(f"[bold bright_white]   ──>[bold yellow] VALIDATING...", end='\r')
            response = requests.get(
                f"{API_URL}/api/profile",
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            data = response.json()
            if data.get('success'):
                CONFIGURATION['user_token'] = token
                user = data['user']
                CONFIGURATION['username'] = user['username']
                CONFIGURATION['total_shares'] = user.get('totalShares', 0)
                CONFIGURATION['member_since'] = user.get('createdAt', 'Unknown')
                self.SAVE_TOKEN(token, user['username'])
                printf(f"[bold bright_white]   ──>[bold green] VALIDATED!", end='\r')
                time.sleep(1)
                return True
            else:
                printf(Panel(f"[bold red]{data.get('message', 'Invalid token!')}", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
                return False
        except:
            printf(Panel(f"[bold red]Connection error!", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
            return False

    def GET_COOKIES_FROM_SERVER(self) -> list:
        try:
            printf(f"[bold bright_white]   ──>[bold yellow] FETCHING COOKIES...", end='\r')
            response = requests.get(
                f"{API_URL}/api/cookies",
                headers={'Authorization': f'Bearer {CONFIGURATION["user_token"]}'},
                timeout=10
            )
            data = response.json()
            if data.get('success') and data.get('cookies'):
                cookies = data['cookies']
                printf(f"[bold bright_white]   ──>[bold green] FOUND {len(cookies)} COOKIES!", end='\r')
                time.sleep(1)
                return cookies
            else:
                printf(f"[bold bright_white]   ──>[bold yellow] NO COOKIES!", end='\r')
                time.sleep(1)
                return []
        except:
            printf(f"[bold bright_white]   ──>[bold red] ERROR FETCHING!", end='\r')
            time.sleep(1)
            return []

    def DELETE_COOKIE_FROM_SERVER(self, cookie_uid: str) -> None:
        try:
            requests.post(
                f"{API_URL}/api/cookies/delete-by-uid",
                headers={'Authorization': f'Bearer {CONFIGURATION["user_token"]}'},
                json={'cookieUid': cookie_uid},
                timeout=10
            )
        except:
            pass

    def UPDATE_SHARES(self, share_count: int) -> None:
        try:
            printf(f"[bold bright_white]   ──>[bold yellow] SYNCING...", end='\r')
            response = requests.post(
                f"{API_URL}/api/update-shares",
                headers={'Authorization': f'Bearer {CONFIGURATION["user_token"]}'},
                json={'shares': share_count},
                timeout=15
            )
            data = response.json()
            if data.get('success'):
                printf(f"[bold bright_white]   ──>[bold green] SYNCED {share_count}!", end='\r')
                time.sleep(1)
        except:
            printf(f"[bold bright_white]   ──>[bold red] SYNC FAILED!", end='\r')
            time.sleep(1)

class FACEBOOK_SHARE:
    def __init__(self) -> None:
        pass

    def TAMPILKAN_LOGO(self) -> None:
        os.system('clear' if os.name == 'posix' else 'cls')
        banner = """
 __   __   ______   ______     ______    
/\ \ / /  /\  ___\ /\  == \   /\  ___\   
\ \ \'/   \ \  __\ \ \  __<   \ \___  \  
 \ \__|    \ \_\    \ \_____\  \/\_____\ 
  \/_/      \/_/     \/_____/   \/_____/
        """
        console.print(f"[bold cyan]{banner}[/bold cyan]")
        console.print("[bold white]Facebook Share Bot v2.0[/bold white]", justify="center")
        console.print("[dim]Multi-Cookie | No Delay | Background Support[/dim]\n", justify="center")

    def TAMPILKAN_PROFILE(self) -> None:
        try:
            member_date = "Unknown"
            if CONFIGURATION['member_since']:
                date_obj = datetime.fromisoformat(CONFIGURATION['member_since'].replace('Z', '+00:00'))
                member_date = date_obj.strftime("%B %Y")
        except:
            member_date = "Unknown"
        printf(Panel(f"""[bold white]Username :[bold green] {CONFIGURATION['username']}
[bold white]Member Since :[bold yellow] {member_date}
[bold white]Total Shares :[bold cyan] {CONFIGURATION['total_shares']:,}""", width=56, style="bold bright_white", title="[bold bright_white][ Profile ]"))

    def GET_PH_TIME(self) -> str:
        ph_tz = pytz.timezone('Asia/Manila')
        return datetime.now(ph_tz).strftime('%I:%M%p').lower()

    async def GET_ACCESS_TOKEN(self, session, cookie: str) -> tuple:
        try:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                'dpr': '1',
                'sec-ch-prefers-color-scheme': 'dark',
                'sec-ch-ua': '"Not(A:Brand";v="24", "Chromium";v="122"',
                'sec-ch-ua-full-version-list': '"Not(A:Brand";v="24.0.0.0", "Chromium";v="122.0.6261.128"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"15.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'viewport-width': '1920',
                'cookie': cookie
            }
            async with session.get('https://business.facebook.com/content_management', headers=headers, timeout=15) as response:
                data = await response.text()
                token_match = re.search(r'EAAG[\w\d]+', data)
                if token_match:
                    return (token_match.group(0), cookie)
                return (None, cookie)
        except:
            return (None, cookie)

    async def SHARE_POST(self, session, cookie: str, cookie_uid: str, access_token: str, target_shares: int, cookie_index: int, auth) -> dict:
        global SUKSES, GAGAL, BLOCKED_COOKIES, RUNNING
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.facebook.com',
            'pragma': 'no-cache',
            'referer': f'https://www.facebook.com/{CONFIGURATION["post"]}',
            'sec-ch-ua': '"Not(A:Brand";v="24", "Chromium";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'x-asbd-id': '129477',
            'x-fb-friendly-name': 'ComposerStoryCreateMutation',
            'x-fb-lsd': 'AVqbxe3J_YA',
            'cookie': cookie
        }
        count = 0
        failed_consecutive = 0
        cookie_blocked = False
        
        while count < target_shares and not cookie_blocked and RUNNING:
            try:
                url = f'https://graph.facebook.com/me/feed?link=https://m.facebook.com/{CONFIGURATION["post"]}&published=0&access_token={access_token}'
                async with session.post(url, headers=headers, timeout=10) as response:
                    data = await response.json()
                    if 'id' in data:
                        count += 1
                        SUKSES.append(data['id'])
                        failed_consecutive = 0
                        progress = (count/target_shares*100)
                        printf(f"[bold bright_white]   ──>[bold green] Cookie #{cookie_index + 1}: {count}/{target_shares} ({progress:.0f}%)", end='\r')
                    else:
                        failed_consecutive += 1
                        GAGAL.append(str(data))
                        if failed_consecutive >= 3:
                            cookie_blocked = True
                            BLOCKED_COOKIES.append({'index': cookie_index, 'uid': cookie_uid})
                            auth.DELETE_COOKIE_FROM_SERVER(cookie_uid)
                            printf(f"[bold bright_white]   ──>[bold red] Cookie #{cookie_index + 1} BLOCKED & DELETED!", end='\r')
                            time.sleep(1)
                            break
            except asyncio.CancelledError:
                break
            except:
                failed_consecutive += 1
                if failed_consecutive >= 3:
                    cookie_blocked = True
                    BLOCKED_COOKIES.append({'index': cookie_index, 'uid': cookie_uid})
                    auth.DELETE_COOKIE_FROM_SERVER(cookie_uid)
                    break
        return {'cookie_index': cookie_index, 'count': count, 'blocked': cookie_blocked, 'cookie_uid': cookie_uid}

    async def START_SHARING(self, target_shares: int, auth) -> None:
        global START_TIME, END_TIME, SUKSES, GAGAL, RUNNING
        START_TIME = self.GET_PH_TIME()
        
        async with aiohttp.ClientSession() as session:
            printf(f"[bold bright_white]   ──>[bold yellow] GETTING TOKENS...", end='\r')
            token_tasks = [self.GET_ACCESS_TOKEN(session, cookie) for cookie in CONFIGURATION['cookies']]
            token_results = await asyncio.gather(*token_tasks)
            
            valid_cookies = []
            for idx, (access_token, cookie) in enumerate(token_results):
                if access_token:
                    cookie_uid = CONFIGURATION['cookie_uids'][idx]
                    valid_cookies.append((cookie, cookie_uid, access_token))
                else:
                    cookie_uid = CONFIGURATION['cookie_uids'][idx]
                    auth.DELETE_COOKIE_FROM_SERVER(cookie_uid)
            
            if not valid_cookies:
                printf(Panel(f"[bold red]No valid cookies!", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
                return
            
            printf(f"[bold bright_white]   ──>[bold green] {len(valid_cookies)} VALID COOKIES!", end='\r')
            time.sleep(1)
            
            share_tasks = []
            for idx, (cookie, cookie_uid, token) in enumerate(valid_cookies):
                task = self.SHARE_POST(session, cookie, cookie_uid, token, target_shares, idx, auth)
                share_tasks.append(task)
            
            results = await asyncio.gather(*share_tasks)
        
        END_TIME = self.GET_PH_TIME()
        total_success = len(SUKSES)
        
        if total_success > 0:
            auth.UPDATE_SHARES(total_success)
        
        blocked_count = len([r for r in results if r['blocked']])
        printf(Panel(f"""[bold white]Start :[bold cyan] {START_TIME}
[bold white]End :[bold green] {END_TIME}
[bold white]Cookies :[bold yellow] {len(valid_cookies)}
[bold white]Blocked :[bold red] {blocked_count}
[bold white]Success :[bold green] {total_success}
[bold white]Failed :[bold red] {len(GAGAL)}""", width=56, style="bold bright_white", title="[bold bright_white][ Summary ]"))

class MAIN:
    def __init__(self) -> None:
        try:
            fb = FACEBOOK_SHARE()
            auth = AUTH()
            
            fb.TAMPILKAN_LOGO()
            if auth.LOAD_TOKEN():
                if not auth.GET_PROFILE():
                    if not auth.INPUT_TOKEN():
                        sys.exit()
            else:
                if not auth.INPUT_TOKEN():
                    sys.exit()
            
            while RUNNING:
                fb.TAMPILKAN_LOGO()
                fb.TAMPILKAN_PROFILE()
                printf(Panel(f"[bold green]1.[bold white] Start Sharing\n[bold cyan]2.[bold white] Check Cookies & Tokens\n[bold yellow]3.[bold white] Update Tool\n[bold red]4.[bold white] Logout", width=56, style="bold bright_white", title="[bold bright_white][ Menu ]", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                choice = console.input("[bold bright_white]   ╰─> ").strip()
                
                if choice == '4':
                    auth.DELETE_TOKEN()
                    printf(Panel(f"[bold green]Logged out!", width=56, style="bold bright_white", title="[bold bright_white][ Success ]"))
                    sys.exit()
                
                elif choice == '2':
                    fb.TAMPILKAN_LOGO()
                    fb.TAMPILKAN_PROFILE()
                    cookies = auth.GET_COOKIES_FROM_SERVER()
                    if cookies:
                        printf(Panel(f"[bold green]Testing {len(cookies)} cookies...", width=56, style="bold bright_white", title="[bold bright_white][ Testing ]"))
                        async def test_cookies():
                            async with aiohttp.ClientSession() as session:
                                tasks = [fb.GET_ACCESS_TOKEN(session, c['cookie']) for c in cookies]
                                results = await asyncio.gather(*tasks)
                                valid = sum(1 for r in results if r[0])
                                return valid
                        valid_count = asyncio.run(test_cookies())
                        printf(Panel(f"[bold white]Total :[bold cyan] {len(cookies)}\n[bold white]Valid :[bold green] {valid_count}\n[bold white]Invalid :[bold red] {len(cookies) - valid_count}", width=56, style="bold bright_white", title="[bold bright_white][ Results ]"))
                    else:
                        printf(Panel(f"[bold red]No cookies found!\n\nUpload cookies at:\n[bold cyan]{API_URL}/profile", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
                    console.input("\n[bold white]Press Enter...")
                    continue
                
                elif choice == '3':
                    fb.TAMPILKAN_LOGO()
                    fb.TAMPILKAN_PROFILE()
                    printf(Panel(f"[bold yellow]Checking for updates...", width=56, style="bold bright_white", title="[bold bright_white][ Update ]"))
                    time.sleep(1)
                    try:
                        if os.system('git rev-parse --git-dir > /dev/null 2>&1') != 0:
                            printf(Panel(f"[bold red]Not a git repository!", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
                            console.input("\nPress Enter...")
                            continue
                        os.system('git fetch origin > /dev/null 2>&1')
                        import subprocess
                        result = subprocess.run(['git', 'rev-list', 'HEAD...origin/main', '--count'], capture_output=True, text=True)
                        if result.stdout.strip() == '0':
                            printf(Panel(f"[bold green]Already up to date!", width=56, style="bold bright_white", title="[bold bright_white][ Success ]"))
                        else:
                            os.system('git pull origin main > /dev/null 2>&1')
                            printf(Panel(f"[bold green]Updated! Restart tool.", width=56, style="bold bright_white", title="[bold bright_white][ Success ]"))
                            time.sleep(2)
                            sys.exit()
                    except:
                        printf(Panel(f"[bold red]Update failed!", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
                    console.input("\nPress Enter...")
                    continue
                
                elif choice == '1':
                    cookies = auth.GET_COOKIES_FROM_SERVER()
                    if not cookies:
                        printf(Panel(f"[bold red]No cookies!\n\nUpload at:\n[bold cyan]{API_URL}/profile", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
                        console.input("\nPress Enter...")
                        continue
                    
                    CONFIGURATION['cookies'] = [c.get('cookie') for c in cookies]
                    CONFIGURATION['cookie_uids'] = [c.get('cookieUid') for c in cookies]
                    
                    fb.TAMPILKAN_LOGO()
                    fb.TAMPILKAN_PROFILE()
                    printf(Panel(f"[bold white]Enter post link:", width=56, style="bold bright_white", title="[bold bright_white][ Post Link ]", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                    post_link = console.input("[bold bright_white]   ╰─> ").strip()
                    if not post_link.startswith('https://'):
                        printf(Panel(f"[bold red]Invalid link!", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
                        console.input("\nPress Enter...")
                        continue
                    CONFIGURATION['post'] = post_link
                    
                    fb.TAMPILKAN_LOGO()
                    fb.TAMPILKAN_PROFILE()
                    printf(Panel(f"[bold white]Shares per cookie:", width=56, style="bold bright_white", title="[bold bright_white][ Count ]", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                    try:
                        share_count = int(console.input("[bold bright_white]   ╰─> ").strip())
                        if share_count <= 0:
                            raise ValueError
                    except:
                        printf(Panel(f"[bold red]Invalid count!", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
                        console.input("\nPress Enter...")
                        continue
                    
                    SUKSES.clear()
                    GAGAL.clear()
                    BLOCKED_COOKIES.clear()
                    
                    fb.TAMPILKAN_LOGO()
                    fb.TAMPILKAN_PROFILE()
                    printf(Panel(f"[bold white]Starting...\n[bold yellow]Press Ctrl+C to stop safely", width=56, style="bold bright_white", title="[bold bright_white][ Starting ]"))
                    time.sleep(2)
                    
                    asyncio.run(fb.START_SHARING(share_count, auth))
                    console.input("\n[bold white]Press Enter...")
                    continue
                else:
                    continue
        except KeyboardInterrupt:
            printf(f"\n[bold yellow]   ──> Stopped by user!")
            time.sleep(1)
            sys.exit()

if __name__ == '__main__':
    MAIN()
