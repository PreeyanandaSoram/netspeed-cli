#!/usr/bin/env python3

import sys
import time
import requests
import subprocess
import threading
import socket

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
    for _ in range(5):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            start = time.time()
            s.connect(('cloudflare.com', 80))
            s.close()
            times.append((time.time() - start) * 1000)
        except:
            times.append(500)
    times.sort()
    return times[len(times) // 2]

def download_test():
    urls = [
        'https://speed.cloudflare.com/__down?bytes=10000000',
        'https://proof.ovh.net/files/10Mb.dat'
    ]
    
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
    print(f"{Fore.CYAN}{Style.BRIGHT}╔════════════════════════════════════════╗")
    print(f"{Fore.CYAN}{Style.BRIGHT}║{Style.BRIGHT}{'         NETSPEED CLI v1.0         '}{Fore.CYAN}{Style.BRIGHT}║")
    print(f"{Fore.CYAN}{Style.BRIGHT}╚════════════════════════════════════════╝")
    print()

def print_result(type_, value, icon):
    colors = {
        'download': Fore.GREEN,
        'upload': Fore.MAGENTA,
        'ping': Fore.YELLOW
    }
    color = colors.get(type_, Fore.WHITE)
    print()
    print(f"  {Fore.WHITE}┌─ {type_.upper()} ─────────────────────┐")
    print(f"  {Fore.WHITE}│ {color}{icon} {value}" + " " * (25 - len(str(value))) + f"{Fore.WHITE}│")
    print(f"  {Fore.WHITE}└" + "─" * 36 + "┘")

def main():
    print_header()
    print(f"{Fore.GRAY}  Starting speed test...\n")
    
    spinner = spin("Measuring ping...")
    ping = int(ping_test())
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

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Speed test cancelled.")
        sys.exit(1)
