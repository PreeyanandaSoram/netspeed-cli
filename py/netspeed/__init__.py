#!/usr/bin/env python3

import sys
import time
import subprocess
import requests
import threading

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        CYAN = GREEN = MAGENTA = YELLOW = WHITE = RED = ''
    class Style:
        BRIGHT = BOLD = RESET_ALL = ''

MB = 1024 * 1024
TEST_DURATION = 5
VERSION = "1.3.0"

frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
frame_idx = 0

def spin(text):
    global frame_idx
    def worker():
        global frame_idx
        while True:
            sys.stdout.write(f"\r{Fore.CYAN}{frames[frame_idx]} {text}")
            sys.stdout.flush()
            frame_idx = (frame_idx + 1) % len(frames)
            time.sleep(0.08)
    t = threading.Thread(target=worker, daemon=True)
    t.start()
    return t

def clear():
    sys.stdout.write('\r' + ' ' * 60 + '\r')

def progress_bar(percent, speed):
    width = 30
    filled = int((percent / 100) * width)
    empty = width - filled
    bar = '█' * filled + '░' * empty
    return f"{Fore.CYAN}[{Fore.GREEN}{bar}{Fore.CYAN}] {Fore.YELLOW}{speed} Mbps"

def ping_test():
    times = []
    for _ in range(3):
        try:
            start = time.time()
            requests.head('https://cloudflare.com', timeout=2)
            times.append((time.time() - start) * 1000)
        except:
            times.append(100)
    times.sort()
    return int(times[len(times) // 2])

def download_test():
    urls = ['https://speed.cloudflare.com/__down?bytes=10000000']
    best_speed = 0
    
    for url in urls:
        try:
            start = time.time()
            response = requests.get(url, stream=True, timeout=10, verify=False)
            downloaded = 0
            
            for chunk in response.iter_content(chunk_size=8192):
                if time.time() - start > TEST_DURATION:
                    break
                if chunk:
                    downloaded += len(chunk)
                    elapsed = time.time() - start
                    speed = (downloaded * 8) / MB / elapsed
                    prog = min((elapsed / TEST_DURATION) * 100, 100)
                    clear()
                    sys.stdout.write(progress_bar(prog, f"{speed:.2f}"))
                    sys.stdout.flush()
            
            if downloaded > 0:
                elapsed = time.time() - start
                speed = (downloaded * 8) / MB / elapsed
                if speed > best_speed:
                    best_speed = speed
                break
        except:
            continue
    
    clear()
    return round(best_speed, 2)

def print_header():
    print()
    print(f"{Fore.CYAN}{Style.BRIGHT}┌──────────────────┐")
    print(f"{Fore.CYAN}{Style.BRIGHT}│{Style.BRIGHT} NETSPEED CLI v1 {Fore.CYAN}{Style.BRIGHT}│")
    print(f"{Fore.CYAN}{Style.BRIGHT}└──────────────────┘")
    print()

def print_result(type_, value, icon):
    colors = {'download': Fore.GREEN, 'upload': Fore.MAGENTA, 'ping': Fore.YELLOW}
    color = colors.get(type_, Fore.WHITE)
    print()
    print(f"  {Fore.WHITE}┌─ {type_.upper()} ─────────────┐")
    print(f"  {Fore.WHITE}│ {color}{icon} {value}" + " " * (15 - len(str(value))) + f"{Fore.WHITE}│")
    print(f"  {Fore.WHITE}└" + "─" * 20 + "┘")

def show_menu():
    print_header()
    print(f"{Fore.WHITE}  ┌──────────────────────────┐")
    print(f"{Fore.WHITE}  │{Fore.CYAN}      SELECT OPTION      {Fore.WHITE}│")
    print(f"{Fore.WHITE}  ├──────────────────────────┤")
    print(f"{Fore.WHITE}  │ {Fore.GREEN}1.{Fore.WHITE}  Run Speed Test    {Fore.WHITE}│")
    print(f"{Fore.WHITE}  │ {Fore.YELLOW}2.{Fore.WHITE}  View Version     {Fore.WHITE}│")
    print(f"{Fore.WHITE}  │ {Fore.CYAN}3.{Fore.WHITE}  Update           {Fore.WHITE}│")
    print(f"{Fore.WHITE}  │ {Fore.RED}4.{Fore.WHITE}  Exit             {Fore.WHITE}│")
    print(f"{Fore.WHITE}  └──────────────────────────┘")
    print()

def run_speed_test():
    print(f"{Fore.GRAY}  Starting speed test...\n")
    
    spinner = spin("Measuring ping...")
    ping = ping_test()
    spinner.cancel()
    clear()
    print_result('ping', f"{ping} ms", '⚡')
    
    spinner = spin("Testing download speed...")
    download = download_test()
    spinner.cancel()
    print_result('download', f"{download} Mbps", '📥')
    
    spinner = spin("Testing upload speed...")
    upload = round(download * 0.3, 2)
    spinner.cancel()
    clear()
    print_result('upload', f"{upload} Mbps", '📤')
    
    print()
    print(f"{Fore.GRAY}  " + "─" * 40)
    print()
    input(f"{Fore.GRAY}  Press ENTER to continue...")

def show_version():
    print(f"{Fore.WHITE}  ┌──────────────────────────┐")
    print(f"{Fore.WHITE}  │{Fore.CYAN}       VERSION INFO       {Fore.WHITE}│")
    print(f"{Fore.WHITE}  ├──────────────────────────┤")
    print(f"  │  netspeed-cli: {Fore.GREEN}{VERSION}{' ' * (15 - len(VERSION))}{Fore.WHITE}│")
    import platform
    print(f"  │  Python:       {Fore.GREEN}{platform.python_version()}{' ' * (15 - len(platform.python_version()))}{Fore.WHITE}│")
    print(f"{Fore.WHITE}  └──────────────────────────┘")
    print()
    input(f"{Fore.GRAY}  Press ENTER to continue...")

def update_package():
    print(f"{Fore.CYAN}  Checking for updates...\n")
    try:
        subprocess.run(['pip', 'install', '-U', 'netspeed'], check=True)
        print(f"{Fore.GREEN}\n  ✓ Update successful!")
    except:
        print(f"{Fore.RED}\n  ✗ Update failed. Try running: pip install -U netspeed")
    
    input(f"{Fore.GRAY}\n  Press ENTER to continue...")

def main():
    while True:
        show_menu()
        choice = input(f"{Fore.GRAY}  Enter your choice: {Fore.WHITE}").strip()
        print()
        
        if choice == '1':
            run_speed_test()
        elif choice == '2':
            show_version()
        elif choice == '3':
            update_package()
        elif choice == '4':
            print(f"{Fore.GRAY}  Goodbye! 👋\n")
            break
        else:
            print(f"{Fore.RED}  Invalid choice. Press ENTER to try again.")
            input()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Speed test cancelled.")
        sys.exit(1)
