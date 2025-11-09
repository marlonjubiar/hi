import requests
import json
from time import sleep

class FBNameChanger:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com"
        
    def get_current_info(self):
        """Get current Facebook profile info"""
        try:
            url = f"{self.base_url}/me"
            params = {
                'fields': 'id,name,first_name,last_name',
                'access_token': self.access_token
            }
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                error = response.json()
                print(f"[-] Error: {error.get('error', {}).get('message', 'Unknown error')}")
                return None
        except Exception as e:
            print(f"[-] Exception: {e}")
            return None
    
    def change_name_with_badge(self, first_name, last_name):
        """Change Facebook name with verified badge"""
        try:
            # Add verified badge to first name
            verified_badge = "󱢏"
            new_first_name = f"{first_name} {verified_badge}"
            
            url = f"{self.base_url}/me"
            payload = {
                'access_token': self.access_token,
                'first_name': new_first_name,
                'last_name': last_name
            }
            
            response = requests.post(url, data=payload)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success', False):
                    return True, "Name changed successfully!"
                else:
                    return False, "Request sent but status unclear"
            else:
                error = response.json()
                error_msg = error.get('error', {}).get('message', 'Unknown error')
                return False, error_msg
                
        except Exception as e:
            return False, str(e)

def print_banner():
    banner = """
╔═══════════════════════════════════════╗
║   FB NAME CHANGER - VERIFIED BADGE    ║
║         Add 󱢏 to Your Name             ║
╚═══════════════════════════════════════╝
    """
    print(banner)

def main():
    print_banner()
    
    print("\n[!] WARNING: Use at your own risk!")
    print("[!] Facebook may remove fake badges and restrict your account\n")
    
    print("[*] Enter your Facebook Access Token:")
    print("[?] Get token from: developers.facebook.com/tools/explorer/")
    access_token = input("\nToken: ").strip()
    
    if not access_token:
        print("\n[-] Access token is required!")
        return
    
    changer = FBNameChanger(access_token)
    
    # Verify token and get current info
    print("\n[*] Verifying access token...")
    current_info = changer.get_current_info()
    
    if not current_info:
        print("[-] Failed to verify token. Make sure:")
        print("    1. Token is valid and not expired")
        print("    2. Token has 'public_profile' permission")
        print("    3. You're connected to the internet")
        return
    
    print(f"[+] Token verified!")
    print(f"[+] Current Name: {current_info.get('name', 'Unknown')}")
    print(f"[+] User ID: {current_info.get('id', 'Unknown')}")
    
    # Get new name
    print("\n[*] Enter new name details:")
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    
    if not first_name or not last_name:
        print("\n[-] Both first name and last name are required!")
        return
    
    # Preview
    print(f"\n[*] Preview: {first_name} 󱢏 {last_name}")
    confirm = input("[?] Proceed with name change? (yes/no): ").strip().lower()
    
    if confirm not in ['yes', 'y']:
        print("\n[*] Cancelled by user")
        return
    
    # Change name
    print("\n[*] Changing name with verified badge...")
    success, message = changer.change_name_with_badge(first_name, last_name)
    
    if success:
        print(f"\n[+] {message}")
        print(f"[+] New Name: {first_name} 󱢏 {last_name}")
        print("\n[!] Important Notes:")
        print("    • Changes may take a few minutes to appear")
        print("    • Facebook may review and remove the badge")
        print("    • You may face restrictions if detected")
        print("    • Name change has a cooldown period")
    else:
        print(f"\n[-] Failed: {message}")
        print("\n[!] Common issues:")
        print("    • Token doesn't have required permissions")
        print("    • You're in name change cooldown period")
        print("    • Facebook detected the badge as invalid")
        print("    • Token expired or invalid")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Interrupted by user")
    except Exception as e:
        print(f"\n[-] Unexpected error: {e}")
