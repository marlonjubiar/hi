#!/usr/bin/env python3
"""
Facebook Cookie Extractor for Termux - Enhanced Version
Usage: python3 fb_login.py
"""

import random
import re
import time
import requests
from typing import Dict, Optional, Tuple
import sys
import json

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
║     Facebook Cookie Extractor v3.0        ║
║         Enhanced Termux Edition           ║
╚═══════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)

class FacebookLogin:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = True
        
    def generate_user_agent(self) -> str:
        """Generate a realistic mobile user agent"""
        agents = [
            "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
        ]
        return random.choice(agents)

    def get_initial_cookies(self, user_agent: str) -> bool:
        """Get initial cookies from Facebook"""
        try:
            headers = {
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            response = self.session.get('https://mbasic.facebook.com/', headers=headers, timeout=15)
            return response.status_code == 200
        except:
            return False

    def extract_form_data(self, html_content: str) -> Dict[str, str]:
        """Extract form data from login page"""
        form_data = {}
        
        # Extract lsd
        lsd_match = re.search(r'name="lsd" value="([^"]*)"', html_content)
        if lsd_match:
            form_data['lsd'] = lsd_match.group(1)
        
        # Extract jazoest
        jazoest_match = re.search(r'name="jazoest" value="([^"]*)"', html_content)
        if jazoest_match:
            form_data['jazoest'] = jazoest_match.group(1)
        
        # Extract m_ts
        m_ts_match = re.search(r'name="m_ts" value="([^"]*)"', html_content)
        if m_ts_match:
            form_data['m_ts'] = m_ts_match.group(1)
        
        # Extract li
        li_match = re.search(r'name="li" value="([^"]*)"', html_content)
        if li_match:
            form_data['li'] = li_match.group(1)
        
        # Extract try_number
        try_match = re.search(r'name="try_number" value="([^"]*)"', html_content)
        if try_match:
            form_data['try_number'] = try_match.group(1)
        else:
            form_data['try_number'] = '0'
        
        # Extract unrecognized_tries
        unrec_match = re.search(r'name="unrecognized_tries" value="([^"]*)"', html_content)
        if unrec_match:
            form_data['unrecognized_tries'] = unrec_match.group(1)
        else:
            form_data['unrecognized_tries'] = '0'
        
        return form_data

    def attempt_login(self, email: str, password: str) -> Tuple[bool, Dict]:
        """Main login method using mbasic.facebook.com"""
        try:
            print(f"{Colors.YELLOW}[*] Initializing session...{Colors.END}")
            user_agent = self.generate_user_agent()
            
            # Get initial cookies
            if not self.get_initial_cookies(user_agent):
                return False, {"error": "Failed to initialize session"}
            
            print(f"{Colors.YELLOW}[*] Fetching login page...{Colors.END}")
            
            headers = {
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://mbasic.facebook.com',
                'Connection': 'keep-alive',
                'Referer': 'https://mbasic.facebook.com/',
                'Upgrade-Insecure-Requests': '1'
            }
            
            # Get login page
            login_page = self.session.get('https://mbasic.facebook.com/login/', headers=headers, timeout=15)
            
            if login_page.status_code != 200:
                return False, {"error": "Failed to load login page"}
            
            print(f"{Colors.YELLOW}[*] Extracting form tokens...{Colors.END}")
            form_data = self.extract_form_data(login_page.text)
            
            if not form_data.get('lsd'):
                return False, {"error": "Failed to extract security tokens"}
            
            print(f"{Colors.YELLOW}[*] Submitting login credentials...{Colors.END}")
            
            # Prepare login data
            login_data = {
                'lsd': form_data.get('lsd', ''),
                'jazoest': form_data.get('jazoest', ''),
                'm_ts': form_data.get('m_ts', ''),
                'li': form_data.get('li', ''),
                'try_number': form_data.get('try_number', '0'),
                'unrecognized_tries': form_data.get('unrecognized_tries', '0'),
                'email': email,
                'pass': password,
                'login': 'Log In'
            }
            
            # Submit login
            login_response = self.session.post(
                'https://mbasic.facebook.com/login/device-based/regular/login/?refsrc=deprecated&lwv=100&refid=8',
                data=login_data,
                headers=headers,
                allow_redirects=True,
                timeout=30
            )
            
            print(f"{Colors.YELLOW}[*] Verifying login status...{Colors.END}")
            
            # Check cookies
            cookies = self.session.cookies.get_dict()
            
            # Check for successful login
            if 'c_user' in cookies and cookies['c_user']:
                print(f"{Colors.YELLOW}[*] Extracting cookies...{Colors.END}")
                
                # Get all important cookies
                important_cookies = {}
                cookie_keys = ['c_user', 'xs', 'fr', 'datr', 'sb', 'wd', 'spin', 'presence']
                
                for key in cookie_keys:
                    if key in cookies:
                        important_cookies[key] = cookies[key]
                
                # Create cookie string
                cookie_string = "; ".join([f"{key}={value}" for key, value in important_cookies.items()])
                uid = cookies.get('c_user', '')
                
                return True, {
                    "success": True,
                    "cookie": cookie_string,
                    "uid": uid,
                    "cookies": important_cookies
                }
            
            # Check for specific errors
            response_text = login_response.text.lower()
            
            if 'checkpoint' in login_response.url or 'checkpoint' in response_text:
                return False, {"error": "Account has security checkpoint. Please verify your account first."}
            
            if 'two_factor' in response_text or 'two-factor' in response_text or 'approvals_code' in response_text:
                return False, {"error": "Two-factor authentication is enabled. Please disable 2FA."}
            
            if 'login_error' in response_text or 'error' in response_text:
                return False, {"error": "Invalid email or password."}
            
            return False, {"error": "Login failed. Please check your credentials."}
            
        except requests.exceptions.Timeout:
            return False, {"error": "Connection timeout. Check your internet."}
        except requests.exceptions.ConnectionError:
            return False, {"error": "Network error. Check your connection."}
        except Exception as e:
            return False, {"error": f"Unexpected error: {str(e)}"}

def save_cookie_to_file(cookie: str, uid: str):
    """Save cookie to file"""
    try:
        filename = f"fb_cookie_{uid}.txt"
        with open(filename, 'w') as f:
            f.write(f"═══════════════════════════════════════\n")
            f.write(f"     Facebook Cookie Extract\n")
            f.write(f"═══════════════════════════════════════\n\n")
            f.write(f"User ID: {uid}\n\n")
            f.write(f"Cookie String:\n")
            f.write(f"{cookie}\n\n")
            f.write(f"═══════════════════════════════════════\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"═══════════════════════════════════════\n")
        return filename
    except Exception as e:
        print(f"{Colors.RED}[!] Error saving to file: {str(e)}{Colors.END}")
        return None

def main():
    """Main function"""
    print_banner()
    
    try:
        # Get email input
        print(f"{Colors.CYAN}[?] Enter Facebook Email/Phone/Username:{Colors.END} ", end='')
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
        
        print(f"\n{Colors.BLUE}{'='*50}{Colors.END}")
        print(f"{Colors.YELLOW}[*] Starting login process...{Colors.END}\n")
        
        # Create login instance and attempt login
        fb_login = FacebookLogin()
        success, result = fb_login.attempt_login(email, password)
        
        print(f"\n{Colors.BLUE}{'='*50}{Colors.END}\n")
        
        if success:
            print(f"{Colors.GREEN}{Colors.BOLD}[✓] LOGIN SUCCESSFUL!{Colors.END}\n")
            print(f"{Colors.CYAN}╔{'═'*48}╗{Colors.END}")
            print(f"{Colors.CYAN}║{Colors.END} {Colors.BOLD}User ID:{Colors.END} {result['uid']:<39} {Colors.CYAN}║{Colors.END}")
            print(f"{Colors.CYAN}╚{'═'*48}╝{Colors.END}\n")
            
            print(f"{Colors.CYAN}Full Cookie String:{Colors.END}")
            print(f"{Colors.WHITE}{result['cookie']}{Colors.END}\n")
            
            # Display individual cookies in a nice format
            print(f"{Colors.CYAN}Individual Cookies:{Colors.END}")
            print(f"{Colors.BLUE}{'─'*50}{Colors.END}")
            for key, value in result['cookies'].items():
                display_value = value[:60] + "..." if len(value) > 60 else value
                print(f"{Colors.YELLOW}{key:12}{Colors.END} : {display_value}")
            print(f"{Colors.BLUE}{'─'*50}{Colors.END}\n")
            
            # Ask to save to file
            print(f"{Colors.CYAN}[?] Save cookie to file? (y/n):{Colors.END} ", end='')
            save_choice = input().strip().lower()
            
            if save_choice == 'y':
                filename = save_cookie_to_file(result['cookie'], result['uid'])
                if filename:
                    print(f"{Colors.GREEN}[✓] Cookie saved to: {filename}{Colors.END}")
            
            print(f"\n{Colors.GREEN}{Colors.BOLD}[✓] Success! You can now use this cookie!{Colors.END}\n")
            
        else:
            print(f"{Colors.RED}{Colors.BOLD}[✗] LOGIN FAILED!{Colors.END}\n")
            print(f"{Colors.RED}Error: {result.get('error', 'Unknown error')}{Colors.END}\n")
            
            print(f"{Colors.YELLOW}╔{'═'*48}╗{Colors.END}")
            print(f"{Colors.YELLOW}║  Troubleshooting Tips{' '*26}║{Colors.END}")
            print(f"{Colors.YELLOW}╚{'═'*48}╝{Colors.END}")
            print(f"  {Colors.CYAN}1.{Colors.END} Double-check your email and password")
            print(f"  {Colors.CYAN}2.{Colors.END} Make sure 2FA is disabled")
            print(f"  {Colors.CYAN}3.{Colors.END} Try logging in via browser first")
            print(f"  {Colors.CYAN}4.{Colors.END} Check for account security checkpoints")
            print(f"  {Colors.CYAN}5.{Colors.END} Use email instead of phone number")
            print(f"  {Colors.CYAN}6.{Colors.END} Verify your internet connection")
            print(f"  {Colors.CYAN}7.{Colors.END} Wait a few minutes and try again\n")
            
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[!] Process interrupted by user.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Fatal error: {str(e)}{Colors.END}")
        sys.exit(1)

if __name__ == '__main__':
    main()
