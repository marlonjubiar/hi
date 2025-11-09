import requests
import json
from time import sleep
import sys

class FBNameChanger:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        })
        
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
                return False, f"Error: {error_msg}"
        except Exception as e:
            return False, f"Exception: {str(e)}"
    
    def change_name_direct(self, first_name, last_name, badge_position="last"):
        """Change Facebook name - tries multiple methods"""
        verified_badge = "󱢏"
        
        # Apply badge based on position
        if badge_position == "last":
            new_first = first_name
            new_last = f"{last_name} {verified_badge}"
        else:
            new_first = f"{first_name} {verified_badge}"
            new_last = last_name
        
        methods = [
            self._method_1(new_first, new_last),
            self._method_2(new_first, new_last),
            self._method_3(new_first, new_last),
        ]
        
        for i, (success, message) in enumerate(methods, 1):
            print(f"[*] Trying method {i}...")
            if success:
                return True, message, f"{new_first} {new_last}"
            sleep(1)
        
        return False, "All methods failed. Facebook is blocking the badge.", None
    
    def _method_1(self, first_name, last_name):
        """Method 1: Standard POST"""
        try:
            url = f"{self.base_url}/me"
            data = {
                'access_token': self.access_token,
                'first_name': first_name,
                'last_name': last_name
            }
            response = self.session.post(url, data=data, timeout=15)
            
            if response.status_code == 200:
                # Verify the change
                sleep(2)
                success, result = self.get_current_info()
                if success and isinstance(result, dict):
                    current_name = result.get('name', '')
                    if "󱢏" in current_name:
                        return True, "Method 1 succeeded!"
                return False, "API accepted but badge was filtered"
            return False, f"Method 1 failed: {response.status_code}"
        except Exception as e:
            return False, f"Method 1 error: {str(e)}"
    
    def _method_2(self, first_name, last_name):
        """Method 2: With locale and method override"""
        try:
            url = f"{self.base_url}/me"
            data = {
                'access_token': self.access_token,
                'first_name': first_name,
                'last_name': last_name,
                'locale': 'en_US',
                'method': 'POST'
            }
            response = self.session.post(url, data=data, timeout=15)
            
            if response.status_code == 200:
                sleep(2)
                success, result = self.get_current_info()
                if success and isinstance(result, dict):
                    current_name = result.get('name', '')
                    if "󱢏" in current_name:
                        return True, "Method 2 succeeded!"
                return False, "API accepted but badge was filtered"
            return False, f"Method 2 failed: {response.status_code}"
        except Exception as e:
            return False, f"Method 2 error: {str(e)}"
    
    def _method_3(self, first_name, last_name):
        """Method 3: Using alternate encoding"""
        try:
            # Try with URL encoding
            url = f"{self.base_url}/me"
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            
            data = {
                'access_token': self.access_token,
                'first_name': first_name,
                'last_name': last_name,
            }
            
            response = self.session.post(url, data=data, headers=headers, timeout=15)
            
            if response.status_code == 200:
                sleep(2)
                success, result = self.get_current_info()
                if success and isinstance(result, dict):
                    current_name = result.get('name', '')
                    if "󱢏" in current_name:
                        return True, "Method 3 succeeded!"
                return False, "API accepted but badge was filtered"
            return False, f"Method 3 failed: {response.status_code}"
        except Exception as e:
            return False, f"Method 3 error: {str(e)}"

def print_banner():
    banner = """
╔═══════════════════════════════════════╗
║   FB NAME CHANGER - VERIFIED BADGE    ║
║      Add 󱢏 to Your Name (v2.0)        ║
╚═══════════════════════════════════════╝
    """
    print(banner)

def main():
    print_banner()
    
    print("\n[!] IMPORTANT NOTICE:")
    print("[!] Facebook's API filters special characters server-side")
    print("[!] This script tries multiple methods but may not work")
    print("[!] Facebook has strengthened protections against fake badges")
    print("[!] Use at your own risk!\n")
    
    # Get access token
    print("[*] Enter your Facebook Access Token:")
    print("[?] Get from: developers.facebook.com/tools/explorer/")
    access_token = input("\nToken: ").strip()
    
    if not access_token:
        print("\n[-] Access token required!")
        sys.exit(1)
    
    changer = FBNameChanger(access_token)
    
    # Verify token
    print("\n[*] Verifying access token...")
    success, result = changer.get_current_info()
    
    if not success:
        print(f"[-] Token verification failed: {result}")
        sys.exit(1)
    
    print(f"[+] Token verified!")
    print(f"[+] Current Name: {result.get('name', 'Unknown')}")
    print(f"[+] User ID: {result.get('id', 'Unknown')}")
    
    # Get new name
    print("\n[*] Enter new name:")
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    
    if not first_name or not last_name:
        print("\n[-] Both names required!")
        sys.exit(1)
    
    # Choose badge position
    print("\n[*] Badge position:")
    print("[1] Last Name (recommended)")
    print("[2] First Name")
    pos_choice = input("\nSelect: ").strip()
    
    badge_pos = "last" if pos_choice == "1" else "first"
    
    # Preview
    if badge_pos == "last":
        preview = f"{first_name} {last_name} 󱢏"
    else:
        preview = f"{first_name} 󱢏 {last_name}"
    
    print(f"\n[*] Preview: {preview}")
    confirm = input("\n[?] Proceed? (yes/no): ").strip().lower()
    
    if confirm not in ['yes', 'y']:
        print("\n[*] Cancelled")
        sys.exit(0)
    
    # Attempt change
    print("\n[*] Attempting to change name with badge...")
    print("[*] Trying multiple methods...\n")
    
    success, message, new_name = changer.change_name_direct(first_name, last_name, badge_pos)
    
    if success:
        print(f"\n[+] SUCCESS! {message}")
        print(f"[+] New Name: {new_name}")
        print("\n[*] Please check your Facebook profile to verify!")
    else:
        print(f"\n[-] FAILED: {message}")
        print("\n[!] Why this happens:")
        print("    • Facebook filters special Unicode characters server-side")
        print("    • The API accepts requests but removes badges automatically")
        print("    • Facebook detects and blocks fake verification badges")
        print("    • This is a security measure to prevent impersonation")
        print("\n[!] Alternative solutions:")
        print("    • Use Facebook's mobile app to change name manually")
        print("    • Some users report success by copying badge from verified profiles")
        print("    • Try changing name through Facebook web (not guaranteed)")
        print("    • Use regular emojis instead (⭐👑💎 etc.)")
        
        # Check if name was changed at all
        print("\n[*] Verifying if any changes were made...")
        success, result = changer.get_current_info()
        if success:
            new_current = result.get('name', '')
            if new_current != f"{result.get('first_name', '')} {result.get('last_name', '')}":
                print(f"[*] Current Name: {new_current}")
                if "󱢏" not in new_current:
                    print("[!] Name changed but badge was filtered by Facebook")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n[-] Error: {e}")
        sys.exit(1)
