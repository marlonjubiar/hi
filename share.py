#!/usr/bin/env python3
"""
Facebook Login Script - Termux Compatible
A command-line tool for Facebook authentication with 2FA support
"""

import hashlib
import uuid
import random
import string
import requests
import json
import sys
from urllib.parse import urlencode

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
║     Facebook Login Tool - Termux         ║
║          2FA Authentication              ║
╚═══════════════════════════════════════════╝
{Colors.END}
    """
    print(banner)

def random_string(length):
    """Generate random alphanumeric string"""
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def encode_sig(data):
    """Encode signature for Facebook API"""
    sorted_data = dict(sorted(data.items()))
    data_str = ''.join(f"{key}={value}" for key, value in sorted_data.items())
    signature = hashlib.md5((data_str + '62f8ce9f74b12f84c123cc23437a4a32').encode()).hexdigest()
    return signature

def convert_cookie(session):
    """Convert session cookies to cookie string"""
    return '; '.join(f"{item['name']}={item['value']}" for item in session)

def convert_token(token):
    """Convert access token to app-specific token"""
    try:
        response = requests.get(
            f"https://api.facebook.com/method/auth.getSessionforApp?format=json&access_token={token}&new_app_id=275254692598279"
        )
        data = response.json()
        if 'error' in data:
            raise Exception(data['error'])
        return data.get('access_token', token)
    except Exception as error:
        print(f"{Colors.YELLOW}[!] Token conversion warning: {str(error)}{Colors.END}")
        return token

def convert_2fa(twofa_code):
    """Convert 2FA code to integer"""
    return int(twofa_code)

def save_result(data, filename="fb_login_result.json"):
    """Save login result to file"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"{Colors.GREEN}[✓] Results saved to: {filename}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[✗] Error saving file: {str(e)}{Colors.END}")

def perform_login(email, password, twofa_code=None):
    """Perform Facebook login"""
    device_id = str(uuid.uuid4())
    adid = str(uuid.uuid4())
    random_str = random_string(24)

    form = {
        'adid': adid,
        'email': email,
        'password': password,
        'format': 'json',
        'device_id': device_id,
        'cpl': 'true',
        'family_device_id': device_id,
        'locale': 'en_US',
        'client_country_code': 'US',
        'credentials_type': 'device_based_login_password',
        'generate_session_cookies': '1',
        'generate_analytics_claim': '1',
        'generate_machine_id': '1',
        'currently_logged_in_userid': '0',
        'irisSeqID': '1',
        'try_num': '1',
        'enroll_misauth': 'false',
        'meta_inf_fbmeta': 'NO_FILE',
        'source': 'login',
        'machine_id': random_str,
        'fb_api_req_friendly_name': 'authenticate',
        'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
        'api_key': '882a8490361da98702bf97a021ddc14d',
        'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
    }

    form['sig'] = encode_sig(form)

    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'x-fb-friendly-name': form['fb_api_req_friendly_name'],
        'x-fb-http-engine': 'Liger',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    url = 'https://b-graph.facebook.com/auth/login'

    print(f"{Colors.CYAN}[*] Attempting login...{Colors.END}")

    try:
        response = requests.post(url, data=urlencode(form), headers=headers)
        response_data = response.json()

        if response.status_code == 200 and 'access_token' in response_data:
            print(f"{Colors.GREEN}[✓] Login successful!{Colors.END}")
            
            if 'session_cookies' in response_data:
                response_data['cookies'] = convert_cookie(response_data['session_cookies'])
            
            if 'access_token' in response_data:
                print(f"{Colors.CYAN}[*] Converting access token...{Colors.END}")
                response_data['access_token'] = convert_token(response_data['access_token'])
            
            return {
                'status': True,
                'message': 'Login successful!',
                'data': response_data
            }

        elif 'error' in response_data:
            error = response_data['error']
            
            if error.get('code') == 401:
                return {
                    'status': False,
                    'message': f"Authentication failed: {error.get('message', 'Invalid credentials')}"
                }
            
            elif error.get('error_subcode') == 1348131:
                print(f"{Colors.YELLOW}[!] 2FA required{Colors.END}")
                
                if not twofa_code:
                    return {
                        'status': False,
                        'message': '2FA code required',
                        'requires_2fa': True,
                        'error_data': error.get('error_data', {})
                    }
                else:
                    return handle_2fa(form, headers, url, twofa_code, error.get('error_data', {}))
            
            else:
                return {
                    'status': False,
                    'message': f"Login error: {error.get('message', 'Unknown error')}"
                }
        else:
            return {
                'status': False,
                'message': 'Unexpected response from Facebook'
            }

    except requests.exceptions.RequestException as e:
        return {
            'status': False,
            'message': f"Network error: {str(e)}"
        }
    except Exception as e:
        return {
            'status': False,
            'message': f"An error occurred: {str(e)}"
        }

def handle_2fa(form, headers, url, twofa_code, error_data):
    """Handle 2FA authentication"""
    try:
        twofa_code_int = convert_2fa(twofa_code)
        
        form['twofactor_code'] = str(twofa_code_int)
        form['encrypted_msisdn'] = ''
        form['userid'] = error_data.get('uid', '')
        form['machine_id'] = error_data.get('machine_id', '')
        form['first_factor'] = error_data.get('login_first_factor', '')
        form['credentials_type'] = 'two_factor'
        form['sig'] = encode_sig(form)

        print(f"{Colors.CYAN}[*] Verifying 2FA code...{Colors.END}")
        
        response2 = requests.post(url, data=urlencode(form), headers=headers)
        
        if response2.status_code == 200:
            data2 = response2.json()
            
            if 'access_token' in data2:
                print(f"{Colors.GREEN}[✓] 2FA verification successful!{Colors.END}")
                
                if 'session_cookies' in data2:
                    data2['cookies'] = convert_cookie(data2['session_cookies'])
                
                if 'access_token' in data2:
                    print(f"{Colors.CYAN}[*] Converting access token...{Colors.END}")
                    data2['access_token'] = convert_token(data2['access_token'])
                
                return {
                    'status': True,
                    'message': 'Login successful with 2FA!',
                    'data': data2
                }
            else:
                return {
                    'status': False,
                    'message': 'Invalid 2FA code or authentication failed'
                }
        else:
            return {
                'status': False,
                'message': 'Authentication failed after 2FA'
            }
    
    except ValueError:
        return {
            'status': False,
            'message': 'Invalid 2FA code format'
        }
    except Exception as error:
        return {
            'status': False,
            'message': f"Error during 2FA authentication: {str(error)}"
        }

def main():
    """Main function"""
    print_banner()
    
    try:
        # Get email
        email = input(f"{Colors.BLUE}[?] Enter Facebook Email/Phone: {Colors.END}").strip()
        if not email:
            print(f"{Colors.RED}[✗] Email/Phone is required!{Colors.END}")
            sys.exit(1)
        
        # Get password
        password = input(f"{Colors.BLUE}[?] Enter Facebook Password: {Colors.END}").strip()
        if not password:
            print(f"{Colors.RED}[✗] Password is required!{Colors.END}")
            sys.exit(1)
        
        # Initial login attempt
        result = perform_login(email, password)
        
        # Check if 2FA is required
        if not result['status'] and result.get('requires_2fa'):
            print(f"\n{Colors.YELLOW}[!] Two-Factor Authentication Required{Colors.END}")
            twofa_code = input(f"{Colors.BLUE}[?] Enter 2FA Code: {Colors.END}").strip()
            
            if twofa_code:
                result = perform_login(email, password, twofa_code)
            else:
                print(f"{Colors.RED}[✗] 2FA code is required!{Colors.END}")
                sys.exit(1)
        
        # Display result
        print(f"\n{Colors.BOLD}{'='*50}{Colors.END}")
        if result['status']:
            print(f"{Colors.GREEN}[✓] SUCCESS: {result['message']}{Colors.END}")
            print(f"\n{Colors.CYAN}Login Data:{Colors.END}")
            
            if 'data' in result:
                data = result['data']
                
                if 'access_token' in data:
                    print(f"{Colors.GREEN}Access Token: {data['access_token'][:50]}...{Colors.END}")
                
                if 'cookies' in data:
                    print(f"{Colors.GREEN}Cookies: {data['cookies'][:100]}...{Colors.END}")
                
                if 'uid' in data:
                    print(f"{Colors.GREEN}User ID: {data['uid']}{Colors.END}")
                
                # Save to file
                save_result(result)
        else:
            print(f"{Colors.RED}[✗] FAILED: {result['message']}{Colors.END}")
        
        print(f"{Colors.BOLD}{'='*50}{Colors.END}\n")
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[!] Script interrupted by user{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[✗] Unexpected error: {str(e)}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
