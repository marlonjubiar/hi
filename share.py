# Check and install required modules
required_modules = {
    'asyncio': 'asyncio',
    'aiohttp': 'aiohttp',
    're': 're',
    'sys': 'sys',
    'os': 'os',
    'time': 'time',
    'json': 'json',
    'requests': 'requests',
    'rich': 'rich',
    'datetime': 'datetime',
    'pytz': 'pytz',
    'concurrent.futures': 'concurrent.futures'
}

missing_modules = []
import sys

print("\n   ──> \033[33mChecking required modules...\033[0m")
import time
time.sleep(0.5)

for module_name, install_name in required_modules.items():
    try:
        if module_name == 'rich':
            __import__('rich.console')
            __import__('rich.panel')
        else:
            __import__(module_name)
        print(f"   ──> \033[32m{module_name} ✓\033[0m" + " " * (30 - len(module_name)), end='\r')
        time.sleep(0.1)
    except ModuleNotFoundError:
        missing_modules.append(install_name)
        print(f"   ──> \033[31m{module_name} ✗ MISSING\033[0m" + " " * (20 - len(module_name)))

if missing_modules:
    print(f"\n   ──> \033[31mFound {len(missing_modules)} missing module(s)\033[0m")
    print(f"   ──> \033[33mInstalling missing modules...\033[0m")
    
    import subprocess
    for module in missing_modules:
        try:
            print(f"   ──> \033[33mInstalling {module}...\033[0m", end='\r')
            subprocess.check_call([sys.executable, "-m", "pip", "install", module, "-q"])
            print(f"   ──> \033[32m{module} installed successfully!\033[0m" + " " * 20)
        except subprocess.CalledProcessError:
            print(f"   ──> \033[31mFailed to install {module}!\033[0m")
            print(f"   ──> \033[33mPlease install manually: pip install {module}\033[0m\n")
            sys.exit(1)
    
    print(f"\n   ──> \033[32mAll modules installed successfully!\033[0m")
    print(f"   ──> \033[32mContinuing to tool...\033[0m\n")
    time.sleep(1.5)
else:
    print(f"\n   ──> \033[32mAll required modules are installed!\033[0m")
    print(f"   ──> \033[32mSUCCESS! You can use the tool now.\033[0m\n")
    time.sleep(1.5)

# Import all modules
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

console = Console()

API_URL = "https://zinktoolsx.onrender.com"
TOKEN_FILE = "Zink/token.json"

CONFIGURATION = {
    'cookies': [],
    'cookie_uids': [],
    'post': None,
    'access_token': None,
    'user_token': None,
    'username': None,
    'user_id': None,
    'total_shares': 0,
    'member_since': None
}

SUKSES, GAGAL, BLOCKED_COOKIES = [], [], []
START_TIME = None
END_TIME = None

# Acquire Termux wake lock to prevent suspension
def acquire_wakelock():
    try:
        import subprocess
        # Try to acquire Termux wake lock
        result = subprocess.run(['termux-wake-lock'], capture_output=True, text=True)
        if result.returncode == 0:
            printf(f"[bold bright_white]   ──>[bold green] WAKE LOCK ACQUIRED! Process won't stop.  ", end='\r')
            time.sleep(1.5)
            return True
        else:
            printf(f"[bold bright_white]   ──>[bold yellow] Wake lock not available. Install termux-api ", end='\r')
            time.sleep(1.5)
            return False
    except Exception as e:
        printf(f"[bold bright_white]   ──>[bold yellow] Wake lock not available.                  ", end='\r')
        time.sleep(1.5)
        return False

# Release Termux wake lock
def release_wakelock():
    try:
        import subprocess
        subprocess.run(['termux-wake-unlock'], capture_output=True)
    except:
        pass

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
            printf(f"[bold bright_white]   ──>[bold yellow] LOADING PROFILE...                   ", end='\r')
            time.sleep(1.0)

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
                
                printf(f"[bold bright_white]   ──>[bold green] PROFILE LOADED SUCCESSFULLY!         ", end='\r')
                time.sleep(1.5)
                return True
            else:
                printf(f"[bold bright_white]   ──>[bold red] {data.get('message', 'FAILED TO LOAD PROFILE!')}              ", end='\r')
                time.sleep(2.0)
                self.DELETE_TOKEN()
                return False
                
        except requests.exceptions.Timeout:
            printf(f"[bold bright_white]   ──>[bold red] CONNECTION TIMEOUT!                  ", end='\r')
            time.sleep(2.0)
            return False
        except requests.exceptions.ConnectionError:
            printf(f"[bold bright_white]   ──>[bold red] CANNOT CONNECT TO SERVER!            ", end='\r')
            time.sleep(2.0)
            return False
        except Exception as e:
            printf(f"[bold bright_white]   ──>[bold red] ERROR: {str(e)[:30]}...              ", end='\r')
            time.sleep(2.0)
            return False

    def INPUT_TOKEN(self) -> bool:
        try:
            printf(Panel(f"[bold white]To use this tool, you need an access token from our website.\n\n[bold cyan]How to get your token:[/bold cyan]\n[bold white]1. Visit[bold yellow] {API_URL}\n[bold white]2. Login or Sign up for an account\n[bold white]3. Go to your profile page\n[bold white]4. Copy your generated token\n[bold white]5. Paste it below", width=56, style="bold bright_white", title="[bold bright_white][ Token Required ]", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
            
            token = console.input("[bold bright_white]   ╰─> ").strip()

            if not token:
                printf(Panel(f"[bold red]Token cannot be empty!", width=56, style="bold bright_white", title="[bold bright_white][ Invalid Input ]"))
                return False

            printf(f"[bold bright_white]   ──>[bold yellow] VALIDATING TOKEN...                  ", end='\r')
            time.sleep(1.0)

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
                
                printf(f"[bold bright_white]   ──>[bold green] TOKEN VALIDATED SUCCESSFULLY!        ", end='\r')
                time.sleep(1.5)
                return True
            else:
                printf(Panel(f"[bold red]{data.get('message', 'Token validation failed!')}", width=56, style="bold bright_white", title="[bold bright_white][ Validation Failed ]"))
                return False
                
        except requests.exceptions.Timeout:
            printf(Panel(f"[bold red]Connection timeout! Please check your internet connection.", width=56, style="bold bright_white", title="[bold bright_white][ Connection Error ]"))
            return False
        except requests.exceptions.ConnectionError:
            printf(Panel(f"[bold red]Cannot connect to server! Please make sure the server is running.", width=56, style="bold bright_white", title="[bold bright_white][ Connection Error ]"))
            return False
        except Exception as e:
            printf(Panel(f"[bold red]{str(e).capitalize()}!", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
            return False

    def GET_COOKIES_FROM_SERVER(self) -> list:
        try:
            printf(f"[bold bright_white]   ──>[bold yellow] FETCHING COOKIES FROM SERVER...      ", end='\r')
            time.sleep(1.0)

            response = requests.get(
                f"{API_URL}/api/cookies",
                headers={'Authorization': f'Bearer {CONFIGURATION["user_token"]}'},
                timeout=10
            )
            
            data = response.json()
            
            if data.get('success') and data.get('cookies'):
                cookies = data['cookies']
                printf(f"[bold bright_white]   ──>[bold green] FOUND {len(cookies)} COOKIES ON SERVER!       ", end='\r')
                time.sleep(1.5)
                return cookies
            else:
                printf(f"[bold bright_white]   ──>[bold yellow] NO COOKIES FOUND ON SERVER!          ", end='\r')
                time.sleep(1.5)
                return []
                
        except Exception as e:
            printf(f"[bold bright_white]   ──>[bold red] ERROR FETCHING COOKIES: {str(e)[:20]}...  ", end='\r')
            time.sleep(2.0)
            return []

    def DELETE_COOKIE_FROM_SERVER(self, cookie_uid: str) -> None:
        try:
            response = requests.post(
                f"{API_URL}/api/cookies/delete-by-uid",
                headers={'Authorization': f'Bearer {CONFIGURATION["user_token"]}'},
                json={'cookieUid': cookie_uid},
                timeout=10
            )
            
            data = response.json()
            if data.get('success'):
                printf(f"[bold bright_white]   ──>[bold green] COOKIE DELETED FROM SERVER!          ", end='\r')
                time.sleep(1.5)
        except Exception as e:
            printf(f"[bold bright_white]   ──>[bold red] ERROR DELETING COOKIE: {str(e)[:20]}...  ", end='\r')
            time.sleep(2.0)

    def UPDATE_SHARES(self, share_count: int) -> None:
        try:
            printf(f"[bold bright_white]   ──>[bold yellow] UPDATING SHARES TO SERVER...         ", end='\r')
            
            response = requests.post(
                f"{API_URL}/api/update-shares",
                headers={'Authorization': f'Bearer {CONFIGURATION["user_token"]}'},
                json={'shares': share_count},
                timeout=15
            )
            
            data = response.json()
            if data.get('success'):
                printf(f"[bold bright_white]   ──>[bold green] {share_count} SHARES UPDATED SUCCESSFULLY!   ", end='\r')
                time.sleep(1.5)
                return True
            else:
                printf(f"[bold bright_white]   ──>[bold red] FAILED TO UPDATE SHARES!             ", end='\r')
                time.sleep(1.5)
                return False
        except Exception as e:
            printf(f"[bold bright_white]   ──>[bold red] ERROR UPDATING SHARES: {str(e)[:20]}... ", end='\r')
            time.sleep(1.5)
            return False

class FACEBOOK_SHARE:

    def __init__(self) -> None:
        pass

    def TAMPILKAN_LOGO(self) -> None:
        os.system('clear' if os.name == 'posix' else 'cls')
        banner_text = """
 __   __   ______   ______     ______    
/\ \ / /  /\  ___\ /\  == \   /\  ___\   
\ \ \'/   \ \  __\ \ \  __<   \ \___  \  
 \ \__|    \ \_\    \ \_____\  \/\_____\ 
  \/_/      \/_/     \/_____/   \/_____/
        """
        console.print(f"[bold cyan]{banner_text}[/bold cyan]")
        console.print("[bold white]Facebook Share Bot v1.0[/bold white]", justify="center")
        console.print("[dim]Automated sharing tool[/dim]\n", justify="center")

    def TAMPILKAN_PROFILE(self) -> None:
        try:
            member_date = "Unknown"
            if CONFIGURATION['member_since']:
                from datetime import datetime
                date_obj = datetime.fromisoformat(CONFIGURATION['member_since'].replace('Z', '+00:00'))
                member_date = date_obj.strftime("%B %Y")
        except:
            member_date = "Unknown"

        printf(Panel(f"""[bold white]Username :[bold green] {CONFIGURATION['username']}
[bold white]Member Since :[bold yellow] {member_date}
[bold white]Total Share :[bold cyan] {CONFIGURATION['total_shares']:,}""", width=56, style="bold bright_white", title="[bold bright_white][ Profile Info ]"))
        
        printf(Panel(f"""[bold white]Use a [bold red]DUMP ACCOUNT[bold white] or an account you don't
actively use - [bold red]NOT YOUR MAIN ACCOUNT[bold white]!

This prevents loss of important information if
the account gets restricted or blocked.""", width=56, style="bold bright_white", title="[bold bright_white][ Important Notice ]"))

    def GET_PH_TIME(self) -> str:
        ph_tz = pytz.timezone('Asia/Manila')
        return datetime.now(ph_tz).strftime('%I:%M%p').lower()

    async def MENDAPATKAN_TOKEN(self, session, cookie: str) -> tuple:
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Google Chrome";v="134", "Chromium";v="134", "Not=A?Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': "Windows",
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'cookie': cookie
            }
            
            async with session.get('https://business.facebook.com/content_management', headers=headers) as response:
                data = await response.text()
                token_match = re.search('EAAG(.*?)","', data)
                
                if not token_match:
                    return (None, cookie)
                
                return ('EAAG' + token_match.group(1), cookie)
                
        except Exception as e:
            return (None, cookie)

    async def MENGIRIM_SHARE_SINGLE(self, session, cookie: str, cookie_uid: str, access_token: str, target_shares: int, cookie_index: int, auth) -> dict:
        global SUKSES, GAGAL, BLOCKED_COOKIES
        
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'accept-encoding': 'gzip, deflate',
            'host': 'b-graph.facebook.com',
            'cookie': cookie
        }
        
        count = 0
        failed_consecutive = 0
        cookie_blocked = False
        
        while count < target_shares and not cookie_blocked:
            try:
                url = f'https://b-graph.facebook.com/me/feed?link=https://mbasic.facebook.com/{CONFIGURATION["post"]}&published=0&access_token={access_token}'
                
                async with session.post(url, headers=headers) as response:
                    data = await response.json()
                    
                    if 'id' in data:
                        count += 1
                        SUKSES.append(data['id'])
                        failed_consecutive = 0
                        
                        printf(Panel(f"""[bold white]Cookie :[bold cyan] #{cookie_index + 1}
[bold white]Status :[bold green] Successfully Shared!
[bold white]Post :[bold red] {CONFIGURATION['post'][:40]}...
[bold white]Progress :[bold yellow] {count}/{target_shares} [bold cyan]({(count/target_shares*100):.1f}%)""", width=56, style="bold bright_white", title="[bold bright_white][ Success ]"))
                        
                    else:
                        failed_consecutive += 1
                        GAGAL.append(str(data))
                        
                        if failed_consecutive >= 3:
                            cookie_blocked = True
                            BLOCKED_COOKIES.append({'index': cookie_index, 'uid': cookie_uid})
                            printf(f"[bold bright_white]   ──>[bold red] COOKIE #{cookie_index + 1} BLOCKED! AUTO-DELETING...  ", end='\r')
                            time.sleep(2.0)
                            
                            auth.DELETE_COOKIE_FROM_SERVER(cookie_uid)
                            break
                    
                    await asyncio.sleep(0)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                failed_consecutive += 1
                GAGAL.append(str(e))
                
                if failed_consecutive >= 3:
                    cookie_blocked = True
                    BLOCKED_COOKIES.append({'index': cookie_index, 'uid': cookie_uid})
                    printf(f"[bold bright_white]   ──>[bold red] COOKIE #{cookie_index + 1} ERROR! AUTO-DELETING...     ", end='\r')
                    time.sleep(2.0)
                    
                    auth.DELETE_COOKIE_FROM_SERVER(cookie_uid)
                    break
        
        return {
            'cookie_index': cookie_index,
            'count': count,
            'blocked': cookie_blocked,
            'cookie_uid': cookie_uid
        }

    async def MENGIRIM_SHARE_MULTI(self, target_shares: int, auth) -> None:
        global START_TIME, END_TIME, SUKSES, GAGAL
        
        START_TIME = self.GET_PH_TIME()
        
        # Set TCP keepalive for connections
        connector = aiohttp.TCPConnector(
            force_close=False,
            enable_cleanup_closed=True,
            keepalive_timeout=300
        )
        
        async with aiohttp.ClientSession(connector=connector) as session:
            printf(f"[bold bright_white]   ──>[bold yellow] GETTING TOKENS FOR ALL COOKIES...    ", end='\r')
            time.sleep(1.0)
            
            token_tasks = [self.MENDAPATKAN_TOKEN(session, cookie) for cookie in CONFIGURATION['cookies']]
            token_results = await asyncio.gather(*token_tasks)
            
            valid_cookies = []
            invalid_cookie_uids = []
            
            for idx, (access_token, cookie) in enumerate(token_results):
                if access_token:
                    cookie_uid = CONFIGURATION['cookie_uids'][idx]
                    valid_cookies.append((cookie, cookie_uid, access_token))
                else:
                    cookie_uid = CONFIGURATION['cookie_uids'][idx]
                    invalid_cookie_uids.append(cookie_uid)
                    printf(f"[bold bright_white]   ──>[bold red] COOKIE #{idx + 1} INVALID! AUTO-DELETING...    ", end='\r')
                    time.sleep(1.5)
                    auth.DELETE_COOKIE_FROM_SERVER(cookie_uid)
            
            if not valid_cookies:
                printf(Panel(f"[bold red]No valid cookies found! All cookies failed to get access token.", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
                return
            
            printf(f"[bold bright_white]   ──>[bold green] FOUND {len(valid_cookies)} VALID COOKIES!        ", end='\r')
            time.sleep(1.5)
            
            printf(f"[bold bright_white]   ──>[bold green] STARTING MULTI-COOKIE SHARING...     ", end='\r')
            time.sleep(1.5)
            
            share_tasks = []
            for idx, (cookie, cookie_uid, token) in enumerate(valid_cookies):
                task = self.MENGIRIM_SHARE_SINGLE(session, cookie, cookie_uid, token, target_shares, idx, auth)
                share_tasks.append(task)
            
            results = await asyncio.gather(*share_tasks)
        
        END_TIME = self.GET_PH_TIME()
        
        total_success = len(SUKSES)
        if total_success > 0:
            auth.UPDATE_SHARES(total_success)
        
        blocked_count = len([r for r in results if r['blocked']])
        
        printf(Panel(f"""[bold white]Start Time :[bold cyan] {START_TIME}
[bold white]End Time :[bold green] {END_TIME}
[bold white]Total Cookies Used :[bold yellow] {len(valid_cookies)}
[bold white]Blocked Cookies :[bold red] {blocked_count}
[bold white]Total Success :[bold green] {total_success}
[bold white]Total Failed :[bold red] {len(GAGAL)}
[bold white]Server Update :[bold green] ✓ Synced""", width=56, style="bold bright_white", title="[bold bright_white][ Final Summary ]"))

class MAIN:

    def __init__(self) -> None:
        try:
            fb = FACEBOOK_SHARE()
            auth = AUTH()
            
            # Initial login/token check
            fb.TAMPILKAN_LOGO()
            
            if auth.LOAD_TOKEN():
                if not auth.GET_PROFILE():
                    if not auth.INPUT_TOKEN():
                        sys.exit()
            else:
                if not auth.INPUT_TOKEN():
                    sys.exit()
            
            # Main menu loop
            while True:
                fb.TAMPILKAN_LOGO()
                fb.TAMPILKAN_PROFILE()
                
                printf(Panel(f"[bold white]What would you like to do?\n\n[bold green]1.[bold white] Start Sharing\n[bold cyan]2.[bold white] Update Tool\n[bold red]3.[bold white] Logout", width=56, style="bold bright_white", title="[bold bright_white][ Menu ]", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                choice = console.input("[bold bright_white]   ╰─> ").strip()
                
                if choice == '3':
                    fb.TAMPILKAN_LOGO()
                    fb.TAMPILKAN_PROFILE()
                    printf(Panel(f"[bold yellow]Are you sure you want to logout?\n\n[bold green]1.[bold white] Yes\n[bold red]2.[bold white] No", width=56, style="bold bright_white", title="[bold bright_white][ Confirm Logout ]", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                    confirm = console.input("[bold bright_white]   ╰─> ").strip()
                    
                    if confirm == '1':
                        auth.DELETE_TOKEN()
                        release_wakelock()
                        fb.TAMPILKAN_LOGO()
                        fb.TAMPILKAN_PROFILE()
                        printf(f"[bold bright_white]   ──>[bold yellow] UPDATING TOOL...                     ", end='\r')
                        time.sleep(1.0)
                        
                        # Pull latest changes
                        pull_result = os.system('git pull origin main > /dev/null 2>&1')
                        
                        if pull_result == 0:
                            fb.TAMPILKAN_LOGO()
                            fb.TAMPILKAN_PROFILE()
                            printf(Panel(f"[bold green]✓ Tool updated successfully!\n\n[bold white]Please restart the tool to apply changes.\n\n[bold yellow]Exiting in 3 seconds...", width=56, style="bold bright_white", title="[bold bright_white][ Update Success ]"))
                            time.sleep(3.0)
                            release_wakelock()
                            sys.exit()
                        else:
                            fb.TAMPILKAN_LOGO()
                            fb.TAMPILKAN_PROFILE()
                            printf(Panel(f"[bold red]Update failed!\n\n[bold white]There might be conflicts or connection issues.\nTry manually updating with:\n[bold cyan]git pull origin main\n\n[bold white]Press Enter to try again...", width=56, style="bold bright_white", title="[bold bright_white][ Update Failed ]"))
                            console.input("")
                            continue
                            
                    except Exception as e:
                        fb.TAMPILKAN_LOGO()
                        fb.TAMPILKAN_PROFILE()
                        printf(Panel(f"[bold red]Error during update!\n\n[bold white]{str(e)[:50]}\n\n[bold white]Press Enter to try again...", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
                        console.input("")
                        continue
                        
                elif choice == '1':
                    # Start sharing process
                    fb.TAMPILKAN_LOGO()
                    fb.TAMPILKAN_PROFILE()
                    
                    # Get cookies from server
                    cookies = auth.GET_COOKIES_FROM_SERVER()
                    
                    if not cookies:
                        fb.TAMPILKAN_LOGO()
                        fb.TAMPILKAN_PROFILE()
                        printf(Panel(f"[bold red]No cookies found on server!\n\nPlease upload your cookies on the website:\n[bold cyan]{API_URL}/profile\n\n[bold white]Press Enter to try again...", width=56, style="bold bright_white", title="[bold bright_white][ No Cookies ]"))
                        console.input("")
                        continue
                    
                    CONFIGURATION['cookies'] = [c.get('cookie') for c in cookies if c.get('cookie')]
                    CONFIGURATION['cookie_uids'] = [c.get('cookieUid') for c in cookies if c.get('cookieUid')]
                    
                    fb.TAMPILKAN_LOGO()
                    fb.TAMPILKAN_PROFILE()
                    printf(Panel(f"[bold green]Found {len(CONFIGURATION['cookies'])} cookies on server!\nAll cookies will be used for sharing.", width=56, style="bold bright_white", title="[bold bright_white][ Cookies Loaded ]"))
                    time.sleep(2.0)
                    
                    # Get post link
                    while True:
                        fb.TAMPILKAN_LOGO()
                        fb.TAMPILKAN_PROFILE()
                        printf(Panel(f"[bold white]Enter the Facebook post link you want to share.\nMake sure the link is correct and starts with https://", width=56, style="bold bright_white", title="[bold bright_white][ Post Link ]", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                        post_link = console.input("[bold bright_white]   ╰─> ").strip()
                        
                        if not post_link:
                            fb.TAMPILKAN_LOGO()
                            fb.TAMPILKAN_PROFILE()
                            printf(Panel(f"[bold red]Post link cannot be empty!\n\n[bold white]Press Enter to try again...", width=56, style="bold bright_white", title="[bold bright_white][ Invalid Input ]"))
                            console.input("")
                            continue
                            
                        if not post_link.startswith('https://'):
                            fb.TAMPILKAN_LOGO()
                            fb.TAMPILKAN_PROFILE()
                            printf(Panel(f"[bold red]Invalid post link! The link must start with https://\n\n[bold white]Press Enter to try again...", width=56, style="bold bright_white", title="[bold bright_white][ Invalid Link ]"))
                            console.input("")
                            continue
                        
                        CONFIGURATION['post'] = post_link
                        break
                    
                    # Get share count
                    while True:
                        fb.TAMPILKAN_LOGO()
                        fb.TAMPILKAN_PROFILE()
                        printf(Panel(f"[bold white]Enter the number of shares you want to send PER COOKIE.\nTotal shares will be: [bold yellow]{len(CONFIGURATION['cookies'])} cookies × your number", width=56, style="bold bright_white", title="[bold bright_white][ Share Count Per Cookie ]", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                        share_count_input = console.input("[bold bright_white]   ╰─> ").strip()
                        
                        if not share_count_input:
                            fb.TAMPILKAN_LOGO()
                            fb.TAMPILKAN_PROFILE()
                            printf(Panel(f"[bold red]Share count cannot be empty!\n\n[bold white]Press Enter to try again...", width=56, style="bold bright_white", title="[bold bright_white][ Invalid Input ]"))
                            console.input("")
                            continue
                        
                        try:
                            share_count = int(share_count_input)
                            if share_count <= 0:
                                fb.TAMPILKAN_LOGO()
                                fb.TAMPILKAN_PROFILE()
                                printf(Panel(f"[bold red]Share count must be greater than 0!\n\n[bold white]Press Enter to try again...", width=56, style="bold bright_white", title="[bold bright_white][ Invalid Count ]"))
                                console.input("")
                                continue
                            break
                        except ValueError:
                            fb.TAMPILKAN_LOGO()
                            fb.TAMPILKAN_PROFILE()
                            printf(Panel(f"[bold red]Invalid share count! Please enter a valid number.\n\n[bold white]Press Enter to try again...", width=56, style="bold bright_white", title="[bold bright_white][ Invalid Input ]"))
                            console.input("")
                            continue
                    
                    # Show configuration and start
                    total_expected = len(CONFIGURATION['cookies']) * share_count
                    
                    fb.TAMPILKAN_LOGO()
                    fb.TAMPILKAN_PROFILE()
                    
                    printf(Panel(f"""[bold white]Total Cookies :[bold cyan] {len(CONFIGURATION['cookies'])}
[bold white]Post Link :[bold yellow] {CONFIGURATION['post'][:35]}...
[bold white]Shares Per Cookie :[bold green] {share_count}
[bold white]Expected Total :[bold red] {total_expected}""", width=56, style="bold bright_white", title="[bold bright_white][ Configuration ]"))
                    
                    printf(Panel(f"[bold white]Multi-cookie sharing will start now!\n[bold yellow]⚠ Blocked cookies will be auto-deleted from server.\n[bold green]✓ All cookies run simultaneously for faster sharing.\n[bold cyan]✓ Process will continue even if you leave Termux!\n\n[bold white]Press Enter to start...", width=56, style="bold bright_white", title="[bold bright_white][ Ready ]"))
                    console.input("")
                    
                    # Acquire wake lock before starting
                    acquire_wakelock()
                    
                    # Reset counters
                    SUKSES.clear()
                    GAGAL.clear()
                    BLOCKED_COOKIES.clear()
                    
                    # Start sharing
                    asyncio.run(fb.MENGIRIM_SHARE_MULTI(share_count, auth))
                    
                    # Release wake lock after completion
                    release_wakelock()
                    
                    # After sharing, ask to continue
                    printf(Panel(f"[bold white]Press Enter to return to menu...", width=56, style="bold bright_white", title="[bold bright_white][ Done ]"))
                    console.input("")
                    continue
                    
                else:
                    fb.TAMPILKAN_LOGO()
                    fb.TAMPILKAN_PROFILE()
                    printf(Panel(f"[bold red]Invalid choice! Please enter 1, 2, or 3.\n\n[bold white]Press Enter to try again...", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
                    console.input("")
                    continue
            
        except KeyboardInterrupt:
            printf(f"\n[bold bright_white]   ──>[bold yellow] PROCESS STOPPED BY USER!             ")
            time.sleep(1.5)
            release_wakelock()
            sys.exit()
        except Exception as e:
            printf(Panel(f"[bold red]{str(e).capitalize()}!", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
            time.sleep(3.0)
            release_wakelock()
            sys.exit()

if __name__ == '__main__':
    MAIN()
        printf(Panel(f"[bold green]Logged out successfully!", width=56, style="bold bright_white", title="[bold bright_white][ Success ]"))
                        sys.exit()
                    else:
                        continue
                
                elif choice == '2':
                    # Update tool
                    fb.TAMPILKAN_LOGO()
                    fb.TAMPILKAN_PROFILE()
                    
                    printf(Panel(f"[bold yellow]Checking for updates...", width=56, style="bold bright_white", title="[bold bright_white][ Update Tool ]"))
                    time.sleep(1.0)
                    
                    try:
                        # Check if git is installed
                        git_check = os.system('git --version > /dev/null 2>&1')
                        
                        if git_check != 0:
                            fb.TAMPILKAN_LOGO()
                            fb.TAMPILKAN_PROFILE()
                            printf(Panel(f"[bold red]Git is not installed on your system!\n\n[bold white]Please install Git first:\n[bold cyan]• Termux: pkg install git\n[bold cyan]• Linux: sudo apt install git\n[bold cyan]• Windows: Download from git-scm.com\n\n[bold white]Press Enter to try again...", width=56, style="bold bright_white", title="[bold bright_white][ Git Not Found ]"))
                            console.input("")
                            continue
                        
                        # Check if current directory is a git repository
                        git_dir_check = os.system('git rev-parse --git-dir > /dev/null 2>&1')
                        
                        if git_dir_check != 0:
                            fb.TAMPILKAN_LOGO()
                            fb.TAMPILKAN_PROFILE()
                            printf(Panel(f"[bold red]This is not a Git repository!\n\n[bold white]To enable auto-updates, clone the repository using:\n[bold cyan]git clone [repository-url]\n\n[bold white]Press Enter to try again...", width=56, style="bold bright_white", title="[bold bright_white][ Not a Git Repository ]"))
                            console.input("")
                            continue
                        
                        fb.TAMPILKAN_LOGO()
                        fb.TAMPILKAN_PROFILE()
                        printf(f"[bold bright_white]   ──>[bold yellow] FETCHING LATEST CHANGES...           ", end='\r')
                        time.sleep(1.0)
                        
                        # Fetch latest changes
                        fetch_result = os.system('git fetch origin > /dev/null 2>&1')
                        
                        if fetch_result != 0:
                            fb.TAMPILKAN_LOGO()
                            fb.TAMPILKAN_PROFILE()
                            printf(Panel(f"[bold red]Failed to fetch updates!\n\n[bold white]Please check your internet connection\nor repository configuration.\n\n[bold white]Press Enter to try again...", width=56, style="bold bright_white", title="[bold bright_white][ Fetch Failed ]"))
                            console.input("")
                            continue
                        
                        # Check if there are updates
                        printf(f"[bold bright_white]   ──>[bold yellow] CHECKING FOR UPDATES...              ", end='\r')
                        time.sleep(1.0)
                        
                        import subprocess
                        result = subprocess.run(['git', 'rev-list', 'HEAD...origin/main', '--count'], 
                                              capture_output=True, text=True)
                        
                        updates_count = result.stdout.strip()
                        
                        if updates_count == '0':
                            fb.TAMPILKAN_LOGO()
                            fb.TAMPILKAN_PROFILE()
                            printf(Panel(f"[bold green]✓ Tool is already up to date!\n\n[bold white]You have the latest version.\n\n[bold white]Press Enter to try again...", width=56, style="bold bright_white", title="[bold bright_white][ Already Updated ]"))
                            console.input("")
                            continue
                        
                        fb.TAMPILKAN_LOGO()
                        fb.TAMPILKAN_PROFILE()
                        printf(Panel(f"[bold green]Updates available!\n\n[bold white]Found [bold yellow]{updates_count}[bold white] new commit(s).\n\n[bold cyan]1.[bold white] Update Now\n[bold red]2.[bold white] Cancel", width=56, style="bold bright_white", title="[bold bright_white][ Updates Found ]", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
                        update_choice = console.input("[bold bright_white]   ╰─> ").strip()
                        
                        if update_choice != '1':
                            continue
                        
                        fb.TAMPILKAN_LOGO()
