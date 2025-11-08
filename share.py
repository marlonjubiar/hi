#!/usr/bin/env python3
"""
Facebook Cookie Extractor for Termux
Usage: python3 fb_login.py
"""

import random
import re
import time
import requests
from typing import Dict, Optional, Tuple
from getpass import getpass
import sys

class Colors:
    """ANSI color codes for terminal"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    """Display script banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════╗
║     Facebook Cookie Extractor v2.0        ║
║         Made for Termux                   ║
╚═══════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)

class FacebookLogin:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
        
    def generate_user_agent(self) -> str:
        """Generate a realistic mobile user agent"""
        android_versions = ['10', '11', '12', '13', '14']
        chrome_versions = range(110, 131)
        
        android_ver = random.choice(android_versions)
        chrome_ver = random.choice(chrome_versions)
        build = random.randint(5000, 6500)
        patch = random.randint(50, 200)
        
        devices = [
            "SM-G960F", "SM-G973F", "SM-G980F", "SM-G991B",
            "SM-A505F", "SM-A515F", "SM-N975F", "SM-N986B",
            "Pixel 5", "Pixel 6", "Pixel 7", "Pixel 8"
        ]
        
        device = random.choice(devices)
        
        return (f"Mozilla/5.0 (Linux; Android {android_ver}; {device}) "
                f"AppleWebKit/537.36 (KHTML, like Gecko) "
                f"Chrome/{chrome_ver}.0.{build}.{patch} Mobile Safari/537.36")

    def extract_form_data(self, html_content: str) -> Dict[str, str]:
        """Extract all necessary tokens from the login page"""
        form_data = {}
        
        # Extract lsd token
        lsd_match = re.search(r'"lsd":"([^"]+)"', html_content)
        if lsd_match:
            form_data['lsd'] = lsd_match.group(1)
        
        # Extract jazoest
        jazoest_match = re.search(r'name="jazoest"\s+value="([^"]+)"', html_content)
        if jazoest_match:
            form_data['jazoest'] = jazoest_match.group(1)
        
        # Extract m_ts
        m_ts_match = re.search(r'name="m_ts"\s+value="([^"]+)"', html_content)
        if m_ts_match:
            form_data['m_ts'] = m_ts_match.group(1)
        
        # Extract li
        li_match = re.search(r'name="li"\s+value="([^"]+)"', html_content)
        if li_match:
            form_data['li'] = li_match.group(1)
        
        # Extract try_number
        try_number_match = re.search(r'name="try_number"\s+value="([^"]+)"', html_content)
        if try_number_match:
            form_data['try_number'] = try_number_match.group(1)
        else:
            form_data['try_number'] = '0'
        
        # Extract unrecognized_tries
        unrecognized_match = re.search(r'name="unrecognized_tries"\s+value="([^"]+)"', html_content)
        if unrecognized_match:
            form_data['unrecognized_tries'] = unrecognized_match.group(1)
        else:
            form_data['unrecognized_tries'] = '0'
            
        return form_data

    def prepare_login_data(self, email: str, password: str, form_data: Dict) -> Dict:
        """Prepare complete login payload"""
        return {
            'lsd': form_data.get('lsd', ''),
            'jazoest': form_data.get('jazoest', ''),
            'm_ts': form_data.get('m_ts', ''),
            'li': form_data.get('li', ''),
            'try_number': form_data.get('try_number', '0'),
            'unrecognized_tries': form_data.get('unrecognized_tries', '0'),
            'email': email,
            'pass': password,
            'login': 'Log In',
            'bi_xrwh': str(random.randint(0, 999999))
        }

    def get_headers(self, user_agent: str, referer: str = None) -> Dict:
        """Generate request headers"""
        headers = {
            'authority': 'm.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://m.facebook.com',
            'referer': referer or 'https://m.facebook.com/',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': user_agent,
        }
        return headers

    def extract_cookies(self) -> Dict[str, str]:
        """Extract important cookies from session"""
        cookies = self.session.cookies.get_dict()
        
        important_cookies = {}
        cookie_keys = ['c_user', 'xs', 'fr', 'datr', 'sb', 'spin', 'wd', 'presence']
        
        for key in cookie_keys:
            if key in cookies:
                important_cookies[key] = cookies[key]
        
        return important_cookies

    def attempt_login(self, email: str, password: str) -> Tuple[bool, Dict]:
        """Main login method"""
        try:
            print(f"{Colors.YELLOW}[*] Generating user agent...{Colors.END}")
            user_agent = self.generate_user_agent()
            
            print(f"{Colors.YELLOW}[*] Fetching login page...{Colors.END}")
            login_page_url = "https://m.facebook.com/login/"
            self.session.headers.update(self.get_headers(user_agent))
            
            initial_response = self.session.get(login_page_url, timeout=15)
            
            if initial_response.status_code != 200:
                return False, {"error": "Failed to load login page"}
            
            print(f"{Colors.YELLOW}[*] Extracting security tokens...{Colors.END}")
            form_data = self.extract_form_data(initial_response.text)
            
            if not form_data.get('lsd'):
                return False, {"error": "Failed to extract required tokens"}
            
            print(f"{Colors.YELLOW}[*] Preparing login request...{Colors.END}")
            login_data = self.prepare_login_data(email, password, form_data)
            
            print(f"{Colors.YELLOW}[*] Attempting login...{Colors.END}")
            login_url = 'https://m.facebook.com/login/device-based/regular/login/?refsrc=deprecated&lwv=100'
            
            login_response = self.session.post(
                login_url,
                data=login_data,
                headers=self.get_headers(user_agent, login_page_url),
                allow_redirects=True,
                timeout=30
            )
            
            print(f"{Colors.YELLOW}[*] Checking login status...{Colors.END}")
            cookies = self.extract_cookies()
            
            if "c_user" in cookies and cookies["c_user"]:
                cookie_string = "; ".join([f"{key}={value}" for key, value in cookies.items()])
                uid = cookies.get('c_user', '')
                
                return True, {
                    "success": True,
                    "cookie": cookie_string,
                    "uid": uid,
                    "cookies": cookies
                }
            
            if "checkpoint" in login_response.url.lower():
                return False, {
                    "error": "Account checkpoint required. Please verify your account through the Facebook app/website first."
                }
            
            if "two_factor" in login_response.text or "two-factor" in login_response.url:
                return False, {
                    "error": "Two-factor authentication is enabled. Please disable 2FA or use app-specific password."
                }
            
            return False, {
                "error": "Invalid email or password. Please check your credentials."
            }
                
        except requests.exceptions.Timeout:
            return False, {"error": "Request timeout. Check your internet connection."}
        except requests.exceptions.ConnectionError:
            return False, {"error": "Connection error. Check your internet connection."}
        except Exception as e:
            return False, {"error": f"Unexpected error: {str(e)}"}

def save_cookie_to_file(cookie: str, uid: str):
    """Save cookie to file"""
    try:
        filename = f"fb_cookie_{uid}.txt"
        with open(filename, 'w') as f:
            f.write(f"User ID: {uid}\n")
            f.write(f"Cookie String:\n{cookie}\n\n")
            f.write(f"Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        return filename
    except Exception as e:
        print(f"{Colors.RED}[!] Error saving to file: {str(e)}{Colors.END}")
        return None

def main():
    """Main function"""
    print_banner()
    
    try:
        # Get email input
        print(f"{Colors.CYAN}[?] Enter your Facebook email/phone:{Colors.END} ", end='')
        email = input().strip()
        
        if not email:
            print(f"{Colors.RED}[!] Email cannot be empty!{Colors.END}")
            sys.exit(1)
        
        # Get password input (visible in Termux)
        print(f"{Colors.CYAN}[?] Enter your Facebook password:{Colors.END} ", end='')
        password = input().strip()
        
        if not password:
            print(f"{Colors.RED}[!] Password cannot be empty!{Colors.END}")
            sys.exit(1)
        
        print(f"\n{Colors.BLUE}{'='*45}{Colors.END}")
        print(f"{Colors.YELLOW}[*] Starting login process...{Colors.END}\n")
        
        # Create login instance and attempt login
        fb_login = FacebookLogin()
        success, result = fb_login.attempt_login(email, password)
        
        print(f"{Colors.BLUE}{'='*45}{Colors.END}\n")
        
        if success:
            print(f"{Colors.GREEN}{Colors.BOLD}[✓] LOGIN SUCCESSFUL!{Colors.END}\n")
            print(f"{Colors.CYAN}User ID:{Colors.END} {result['uid']}")
            print(f"\n{Colors.CYAN}Cookie String:{Colors.END}")
            print(f"{Colors.WHITE}{result['cookie']}{Colors.END}\n")
            
            # Display individual cookies
            print(f"{Colors.CYAN}Individual Cookies:{Colors.END}")
            for key, value in result['cookies'].items():
                print(f"  {Colors.YELLOW}{key}:{Colors.END} {value[:50]}..." if len(value) > 50 else f"  {Colors.YELLOW}{key}:{Colors.END} {value}")
            
            # Ask to save to file
            print(f"\n{Colors.CYAN}[?] Save cookie to file? (y/n):{Colors.END} ", end='')
            save_choice = input().strip().lower()
            
            if save_choice == 'y':
                filename = save_cookie_to_file(result['cookie'], result['uid'])
                if filename:
                    print(f"{Colors.GREEN}[✓] Cookie saved to: {filename}{Colors.END}")
            
            print(f"\n{Colors.GREEN}[✓] You can now use this cookie for automation!{Colors.END}")
            
        else:
            print(f"{Colors.RED}{Colors.BOLD}[✗] LOGIN FAILED!{Colors.END}\n")
            print(f"{Colors.RED}Error: {result.get('error', 'Unknown error')}{Colors.END}")
            
            print(f"\n{Colors.YELLOW}Troubleshooting tips:{Colors.END}")
            print(f"  1. Double-check your email and password")
            print(f"  2. Disable Two-Factor Authentication (2FA)")
            print(f"  3. Try logging in through browser first")
            print(f"  4. Check if your account has security checkpoint")
            print(f"  5. Make sure you have stable internet connection\n")
            
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[!] Process interrupted by user.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[!] An error occurred: {str(e)}{Colors.END}")
        sys.exit(1)

if __name__ == '__main__':
    main()
