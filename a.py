import requests
import json
from time import sleep
import sys

class FBNameChanger:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com"
        self.session = requests.Session()
        
    def get_current_info(self):
        """Get current Facebook profile info"""
        try:
            url = f"{self.base_url}/me"
            params = {
                'fields': 'id,name,first_name,last_name',
                'access_token': self.access_token
            }
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return True, response.json()
            else:
                error = response.json()
                error_msg = error.get('error', {}).get('message', 'Unknown error')
                error_code = error.get('error', {}).get('code', 'N/A')
                return False, f"Error {error_code}: {error_msg}"
        except requests.exceptions.Timeout:
            return False, "Request timeout. Check your internet connection."
        except requests.exceptions.ConnectionError:
            return False, "Connection error. Check your internet connection."
        except Exception as e:
            return False, f"Exception: {str(e)}"
    
    def change_name_with_badge(self, first_name, last_name):
        """Change Facebook name with verified badge on LAST NAME"""
        try:
            # Add verified badge to LAST name
            verified_badge = "󱢏"
            new_last_name = f"{last_name} {verified_badge}"
            
            url = f"{self.base_url}/me"
            payload = {
                'access_token': self.access_token,
                'first_name': first_name,
                'last_name': new_last_name,
                'method': 'POST'
            }
            
            response = self.session.post(url, data=payload, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success', False) or result == True:
                    return True, "Name changed successfully!", f"{first_name} {new_last_name}"
                else:
                    return False, "Request completed but success status uncertain", None
            else:
                error = response.json()
                error_msg = error.get('error', {}).get('message', 'Unknown error')
                error_code = error.get('error', {}).get('code', 'N/A')
                error_type = error.get('error', {}).get('type', 'Unknown')
                
                # Detailed error messages
                if error_code == 190:
                    return False, "Invalid or expired access token. Please get a new token.", None
                elif error_code == 100:
                    return False, "Invalid parameter. The name may violate Facebook's policies.", None
                elif "OAuthException" in error_type:
                    return False, f"Authentication error: {error_msg}", None
                else:
                    return False, f"Error {error_code}: {error_msg}", None
                    
        except requests.exceptions.Timeout:
            return False, "Request timeout. Please try again.", None
        except requests.exceptions.ConnectionError:
            return False, "Connection error. Check your internet connection.", None
        except Exception as e:
            return False, f"Unexpected error: {str(e)}", None

def print_banner():
    banner = """
╔═══════════════════════════════════════╗
║   FB NAME CHANGER - VERIFIED BADGE    ║
║      Add 󱢏 to Your LAST Name          ║
╚═══════════════════════════════════════╝
    """
    print(banner)

def validate_input(text, field_name):
    """Validate user input"""
    if not text or text.strip() == "":
        return False, f"{field_name} cannot be empty"
    if len(text) > 50:
        return False, f"{field_name} is too long (max 50 characters)"
    if len(text) < 2:
        return False, f"{field_name} is too short (min 2 characters)"
    return True, "Valid"

def main():
    print_banner()
    
    print("\n[!] WARNING: Use at your own risk!")
    print("[!] Facebook may remove fake badges and restrict your account")
    print("[!] The verified badge will be added to your LAST NAME\n")
    
    # Get access token
    print("[*] Enter your Facebook Access Token:")
    print("[?] Get token from: developers.facebook.com/tools/explorer/")
    access_token = input("\nToken: ").strip()
    
    if not access_token:
        print("\n[-] Access token is required!")
        sys.exit(1)
    
    if len(access_token) < 50:
        print("\n[!] Warning: Token seems too short. Are you sure it's correct?")
        confirm = input("[?] Continue anyway? (yes/no): ").strip().lower()
        if confirm not in ['yes', 'y']:
            print("\n[*] Cancelled by user")
            sys.exit(0)
    
    changer = FBNameChanger(access_token)
    
    # Verify token and get current info
    print("\n[*] Verifying access token...")
    success, result = changer.get_current_info()
    
    if not success:
        print(f"[-] Failed to verify token: {result}")
        print("\n[!] Troubleshooting:")
        print("    1. Make sure token is valid and not expired")
        print("    2. Token needs 'public_profile' permission")
        print("    3. Check your internet connection")
        print("    4. Try generating a new token")
        sys.exit(1)
    
    current_info = result
    print(f"[+] Token verified successfully!")
    print(f"[+] Current Name: {current_info.get('name', 'Unknown')}")
    print(f"[+] User ID: {current_info.get('id', 'Unknown')}")
    
    # Get new name with validation
    print("\n[*] Enter new name details:")
    
    first_name = input("First Name: ").strip()
    valid, message = validate_input(first_name, "First name")
    if not valid:
        print(f"\n[-] {message}")
        sys.exit(1)
    
    last_name = input("Last Name: ").strip()
    valid, message = validate_input(last_name, "Last name")
    if not valid:
        print(f"\n[-] {message}")
        sys.exit(1)
    
    # Preview with badge on LAST name
    print(f"\n[*] Preview: {first_name} {last_name} 󱢏")
    print(f"[*] Badge will be added to: LAST NAME")
    confirm = input("\n[?] Proceed with name change? (yes/no): ").strip().lower()
    
    if confirm not in ['yes', 'y']:
        print("\n[*] Cancelled by user")
        sys.exit(0)
    
    # Change name
    print("\n[*] Changing name with verified badge on last name...")
    print("[*] Please wait...")
    
    success, message, new_name = changer.change_name_with_badge(first_name, last_name)
    
    if success:
        print(f"\n[+] SUCCESS! {message}")
        print(f"[+] New Name: {new_name}")
        print("\n[!] Important Notes:")
        print("    • Changes may take 1-5 minutes to appear")
        print("    • Check your profile to verify the change")
        print("    • Facebook may review and remove the badge")
        print("    • You may face account restrictions if detected")
        print("    • Name changes have cooldown periods (60 days)")
        print("\n[*] Done!")
    else:
        print(f"\n[-] FAILED: {message}")
        print("\n[!] Common Issues & Solutions:")
        print("    • Invalid Token → Get a new token from Graph API Explorer")
        print("    • Cooldown Period → Wait 60 days from last name change")
        print("    • Permissions Missing → Grant all required permissions")
        print("    • Badge Detected → Facebook may block special characters")
        print("    • Policy Violation → Name must follow Facebook's rules")
        print("\n[?] Need help? Check Facebook's name policy at:")
        print("    facebook.com/help/112146705538576")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[-] Unexpected error: {e}")
        print("[!] Please report this error if it persists")
        sys.exit(1)
