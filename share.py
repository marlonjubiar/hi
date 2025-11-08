#!/usr/bin/env python3
"""
Facebook Login Script - Enhanced Version with OAuth
Reliable authentication with advanced headers and UID extraction
"""

import hashlib
import uuid
import random
import string
import requests
import json
import sys
import re
from urllib.parse import urlencode, quote
from datetime import datetime

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """Display script banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════╗
║   Facebook Login Tool - Enhanced v2.0    ║
║     OAuth & UID Extraction Support       ║
╚═══════════════════════════════════════════╝
{Colors.END}
    """
    print(banner)

def random_string(length):
    """Generate random alphanumeric string"""
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_device_id():
    """Generate realistic device ID"""
    return str(uuid.uuid4())

def get_timestamp():
    """Get current timestamp"""
    return str(int(datetime.now().timestamp()))

def encode_sig(data):
    """Encode signature for Facebook API"""
    sorted_data = dict(sorted(data.items()))
    data_str = ''.join(f"{key}={value}" for key, value in sorted_data.items())
    signature = hashlib.md5((data_str + '62f8ce9f74b12f84c123cc23437a4a32').encode()).hexdigest()
    return signature

def convert_cookie(session):
    """Convert session cookies to cookie string"""
    return '; '.join(f"{item['name']}={item['value']}" for item in session)

def extract_uid_from_token(token):
    """Extract UID from access token"""
    try:
        parts = token.split('|')
        if len(parts) >= 2:
            uid = parts[0]
            if uid.isdigit():
                return uid
    except:
        pass
    return None

def get_uid_from_cookies(cookies_dict):
    """Extract UID from cookies"""
    for cookie in cookies_dict:
        if cookie.get('name') == 'c_user':
            return cookie.get('value')
    return None

def convert_token(token):
    """Convert access token to app-specific token with OAuth"""
    try:
        print(f"{Colors.CYAN}[*] Converting token via OAuth...{Colors.END}")
        
        # Method 1: Try getSessionforApp
        response = requests.get(
            f"https://api.facebook.com/method/auth.getSessionforApp",
            params={
                'format': 'json',
                'access_token': token,
                'new_app_id': '275254692598279'
            },
            timeout=10
        )
        
        data = response.json()
        if 'access_token' in data:
            return data['access_token']
        
        # Method 2: Try OAuth endpoint
        oauth_url = "https://graph.facebook.com/v18.0/oauth/access_token"
        oauth_response = requests.get(
            oauth_url,
            params={
                'grant_type': 'fb_exchange_token',
                'client_id': '882a8490361da98702bf97a021ddc14d',
                'client_secret': '62f8ce9f74b12f84c123cc23437a4a32',
                'fb_exchange_token': token
            },
            timeout=10
        )
        
        oauth_data = oauth_response.json()
        if 'access_token' in oauth_data:
            return oauth_data['access_token']
        
        return token
        
    except Exception as error:
        print(f"{Colors.YELLOW}[!] Token conversion warning: {str(error)}{Colors.END}")
        return token

def get_advanced_headers(friendly_name):
    """Generate advanced headers for better reliability"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-FB-Friendly-Name': friendly_name,
        'X-FB-HTTP-Engine': 'Liger',
        'X-FB-Client-IP': 'True',
        'X-FB-Server-Cluster': 'True',
        'X-FB-Connection-Type': 'WIFI',
        'X-Tigon-Is-Retry': 'False',
        'X-FB-Request-Analytics-Tags': 'unknown',
        'X-FB-Background-State': '1',
        'X-FB-Net-HNI': '45201',
        'X-FB-SIM-HNI': '45201',
        'Authorization': 'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32',
        'X-FB-Device-Group': '5300',
        'Accept-Language': 'en-US',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }
    return headers

def get_user_info(access_token):
    """Get user information including UID"""
    try:
        print(f"{Colors.CYAN}[*] Fetching user information...{Colors.END}")
        
        # Try Graph API
        response = requests.get(
            'https://graph.facebook.com/me',
            params={
                'access_token': access_token,
                'fields': 'id,name,email,first_name,last_name'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            return user_data
        
        return None
        
    except Exception as e:
        print(f"{Colors.YELLOW}[!] Could not fetch user info: {str(e)}{Colors.END}")
        return None

def perform_login(email, password, twofa_code=None):
    """Perform Facebook login with enhanced authentication"""
    device_id = generate_device_id()
    adid = generate_device_id()
    family_device_id = generate_device_id()
    random_str = random_string(24)
    
    form = {
        'adid': adid,
        'email': email,
        'password': password,
        'format': 'json',
        'device_id': device_id,
        'cpl': 'true',
        'family_device_id': family_device_id,
        'credentials_type': 'device_based_login_password',
        'generate_session_cookies': '1',
        'generate_analytics_claim': '1',
        'generate_machine_id': '1',
        'currently_logged_in_userid': '0',
        'locale': 'en_US',
        'client_country_code': 'US',
        'method': 'auth.login',
        'fb_api_req_friendly_name': 'authenticate',
        'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
        'api_key': '882a8490361da98702bf97a021ddc14d',
        'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
        'irisSeqID': '1',
        'try_num': '1',
        'enroll_misauth': 'false',
        'meta_inf_fbmeta': 'NO_FILE',
        'source': 'login',
        'machine_id': random_str,
        'meta_inf_fbmeta': '',
        'advertiser_id': adid,
        'encrypted_msisdn': '',
    }

    form['sig'] = encode_sig(form)
    
    headers = get_advanced_headers(form['fb_api_req_friendly_name'])

    url = 'https://b-graph.facebook.com/auth/login'

    print(f"{Colors.CYAN}[*] Initiating login request...{Colors.END}")
    print(f"{Colors.CYAN}[*] Device ID: {device_id[:20]}...{Colors.END}")

    try:
        response = requests.post(url, data=urlencode(form), headers=headers, timeout=30)
        
        try:
            response_data = response.json()
        except:
            return {
                'status': False,
                'message': 'Invalid response from server'
            }

        # Successful login
        if response.status_code == 200 and 'access_token' in response_data:
            print(f"{Colors.GREEN}[✓] Login successful!{Colors.END}")
            
            # Extract UID from various sources
            uid = None
            
            # Method 1: From session_cookies
            if 'session_cookies' in response_data:
                response_data['cookies'] = convert_cookie(response_data['session_cookies'])
                uid = get_uid_from_cookies(response_data['session_cookies'])
                print(f"{Colors.GREEN}[✓] UID extracted from cookies: {uid}{Colors.END}")
            
            # Method 2: From token
            if not uid and 'access_token' in response_data:
                uid = extract_uid_from_token(response_data['access_token'])
                if uid:
                    print(f"{Colors.GREEN}[✓] UID extracted from token: {uid}{Colors.END}")
            
            # Method 3: From uid field
            if not uid and 'uid' in response_data:
                uid = response_data['uid']
                print(f"{Colors.GREEN}[✓] UID found in response: {uid}{Colors.END}")
            
            # Store UID
            if uid:
                response_data['uid'] = uid
            
            # Convert token with OAuth
            if 'access_token' in response_data:
                original_token = response_data['access_token']
                converted_token = convert_token(original_token)
                response_data['access_token'] = converted_token
                response_data['original_token'] = original_token
                
                # Get user info
                user_info = get_user_info(converted_token)
                if user_info:
                    response_data['user_info'] = user_info
                    if not uid and 'id' in user_info:
                        response_data['uid'] = user_info['id']
                        uid = user_info['id']
                        print(f"{Colors.GREEN}[✓] UID from Graph API: {uid}{Colors.END}")
            
            return {
                'status': True,
                'message': 'Login successful!',
                'data': response_data
            }

        # Error handling
        elif 'error' in response_data:
            error = response_data['error']
            error_msg = error.get('message', 'Unknown error')
            error_code = error.get('code', 0)
            error_subcode = error.get('error_subcode', 0)
            
            print(f"{Colors.YELLOW}[!] Error Code: {error_code}, Subcode: {error_subcode}{Colors.END}")
            
            # Invalid credentials
            if error_code == 401 or error_code == 400:
                return {
                    'status': False,
                    'message': f"Authentication failed: {error_msg}"
                }
            
            # 2FA required
            elif error_subcode == 1348131 or 'two_factor' in str(error_msg).lower():
                print(f"{Colors.YELLOW}[!] Two-factor authentication required{Colors.END}")
                
                if not twofa_code:
                    return {
                        'status': False,
                        'message': '2FA code required',
                        'requires_2fa': True,
                        'error_data': error.get('error_data', {})
                    }
                else:
                    return handle_2fa(form, headers, url, twofa_code, error.get('error_data', {}))
            
            # Checkpoint required
            elif error_subcode == 1348092 or 'checkpoint' in str(error_msg).lower():
                return {
                    'status': False,
                    'message': 'Account checkpoint required. Please verify your account on Facebook.'
                }
            
            else:
                return {
                    'status': False,
                    'message': f"Login error: {error_msg}"
                }
        else:
            return {
                'status': False,
                'message': 'Unexpected response from Facebook'
            }

    except requests.exceptions.Timeout:
        return {
            'status': False,
            'message': 'Connection timeout. Please check your internet connection.'
        }
    except requests.exceptions.ConnectionError:
        return {
            'status': False,
            'message': 'Connection error. Please check your internet connection.'
        }
    except Exception as e:
        return {
            'status': False,
            'message': f"An error occurred: {str(e)}"
        }

def handle_2fa(form, headers, url, twofa_code, error_data):
    """Handle 2FA authentication with enhanced headers"""
    try:
        twofa_code_int = int(twofa_code)
        
        # Update form for 2FA
        form['twofactor_code'] = str(twofa_code_int)
        form['encrypted_msisdn'] = ''
        form['userid'] = error_data.get('uid', '')
        form['machine_id'] = error_data.get('machine_id', form.get('machine_id', ''))
        form['first_factor'] = error_data.get('login_first_factor', '')
        form['credentials_type'] = 'two_factor'
        form['password'] = form.get('password', '')
        
        # Regenerate signature
        form['sig'] = encode_sig(form)

        print(f"{Colors.CYAN}[*] Verifying 2FA code: {twofa_code}{Colors.END}")
        
        response2 = requests.post(url, data=urlencode(form), headers=headers, timeout=30)
        
        if response2.status_code == 200:
            data2 = response2.json()
            
            if 'access_token' in data2:
                print(f"{Colors.GREEN}[✓] 2FA verification successful!{Colors.END}")
                
                # Extract UID
                uid = None
                if 'session_cookies' in data2:
                    data2['cookies'] = convert_cookie(data2['session_cookies'])
                    uid = get_uid_from_cookies(data2['session_cookies'])
                
                if not uid and 'uid' in data2:
                    uid = data2['uid']
                
                if not uid:
                    uid = extract_uid_from_token(data2.get('access_token', ''))
                
                if uid:
                    data2['uid'] = uid
                    print(f"{Colors.GREEN}[✓] UID: {uid}{Colors.END}")
                
                # Convert token
                if 'access_token' in data2:
                    original_token = data2['access_token']
                    converted_token = convert_token(original_token)
                    data2['access_token'] = converted_token
                    data2['original_token'] = original_token
                    
                    # Get user info
                    user_info = get_user_info(converted_token)
                    if user_info:
                        data2['user_info'] = user_info
                        if not uid and 'id' in user_info:
                            data2['uid'] = user_info['id']
                
                return {
                    'status': True,
                    'message': 'Login successful with 2FA!',
                    'data': data2
                }
            else:
                error_msg = data2.get('error', {}).get('message', 'Invalid 2FA code')
                return {
                    'status': False,
                    'message': f'2FA failed: {error_msg}'
                }
        else:
            return {
                'status': False,
                'message': 'Authentication failed after 2FA'
            }
    
    except ValueError:
        return {
            'status': False,
            'message': 'Invalid 2FA code format. Please enter numbers only.'
        }
    except Exception as error:
        return {
            'status': False,
            'message': f"Error during 2FA authentication: {str(error)}"
        }

def save_result(data, filename="fb_login_result.json"):
    """Save login result to file"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"{Colors.GREEN}[✓] Results saved to: {filename}{Colors.END}")
        return True
    except Exception as e:
        print(f"{Colors.RED}[✗] Error saving file: {str(e)}{Colors.END}")
        return False

def display_result(result):
    """Display formatted result"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    
    if result['status']:
        print(f"{Colors.GREEN}{Colors.BOLD}[✓] SUCCESS: {result['message']}{Colors.END}")
        
        if 'data' in result:
            data = result['data']
            
            print(f"\n{Colors.CYAN}{Colors.BOLD}━━━ Account Information ━━━{Colors.END}")
            
            # UID
            if 'uid' in data:
                print(f"{Colors.GREEN}User ID (UID): {Colors.BOLD}{data['uid']}{Colors.END}")
            
            # User Info
            if 'user_info' in data:
                user = data['user_info']
                if 'name' in user:
                    print(f"{Colors.GREEN}Name: {user['name']}{Colors.END}")
                if 'email' in user:
                    print(f"{Colors.GREEN}Email: {user['email']}{Colors.END}")
            
            print(f"\n{Colors.CYAN}{Colors.BOLD}━━━ Authentication Tokens ━━━{Colors.END}")
            
            # Access Token
            if 'access_token' in data:
                token = data['access_token']
                print(f"{Colors.GREEN}Access Token: {token[:60]}...{Colors.END}")
            
            # Original Token
            if 'original_token' in data:
                print(f"{Colors.YELLOW}Original Token: {data['original_token'][:60]}...{Colors.END}")
            
            # Cookies
            if 'cookies' in data:
                cookies = data['cookies']
                print(f"\n{Colors.CYAN}{Colors.BOLD}━━━ Session Cookies ━━━{Colors.END}")
                print(f"{Colors.GREEN}{cookies[:200]}...{Colors.END}")
            
            # Machine ID
            if 'machine_id' in data:
                print(f"\n{Colors.CYAN}Machine ID: {data['machine_id']}{Colors.END}")
            
            print(f"\n{Colors.GREEN}{Colors.BOLD}[✓] All data saved to fb_login_result.json{Colors.END}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}[✗] FAILED: {result['message']}{Colors.END}")
    
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")

def main():
    """Main function"""
    print_banner()
    
    try:
        # Get email
        email = input(f"{Colors.BLUE}{Colors.BOLD}[?] Facebook Email/Phone/Username: {Colors.END}").strip()
        if not email:
            print(f"{Colors.RED}[✗] Email/Phone is required!{Colors.END}")
            sys.exit(1)
        
        # Get password
        password = input(f"{Colors.BLUE}{Colors.BOLD}[?] Facebook Password: {Colors.END}").strip()
        if not password:
            print(f"{Colors.RED}[✗] Password is required!{Colors.END}")
            sys.exit(1)
        
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        
        # Initial login attempt
        result = perform_login(email, password)
        
        # Check if 2FA is required
        if not result['status'] and result.get('requires_2fa'):
            print(f"\n{Colors.YELLOW}{Colors.BOLD}[!] Two-Factor Authentication Required{Colors.END}")
            print(f"{Colors.YELLOW}Please check your authentication app or SMS{Colors.END}\n")
            
            twofa_code = input(f"{Colors.BLUE}{Colors.BOLD}[?] Enter 6-digit 2FA Code: {Colors.END}").strip()
            
            if twofa_code and len(twofa_code) >= 6:
                print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
                result = perform_login(email, password, twofa_code)
            else:
                print(f"{Colors.RED}[✗] Invalid 2FA code!{Colors.END}")
                sys.exit(1)
        
        # Display and save result
        display_result(result)
        
        if result['status']:
            save_result(result)
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[!] Script interrupted by user{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[✗] Unexpected error: {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
