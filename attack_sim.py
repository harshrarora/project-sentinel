#!/usr/bin/env python3
"""
Simulated Mirai-style attacker for demo purposes
Attempts brute-force login against Sentinel honeypot
"""
import socket
import time
import sys

TARGET_IP = "127.0.0.1"
TARGET_PORT = 2323

# Common IoT default credentials (Mirai-style)
CREDENTIALS = [
    ("admin", "admin"),
    ("root", "root"),
    ("admin", "12345"),
    ("admin", "password"),
    ("user", "user"),
]

def print_banner():
    print("=" * 60)
    print("  SIMULATED ATTACKER - Mirai-style IoT Botnet")
    print("=" * 60)
    print(f"  Target: {TARGET_IP}:{TARGET_PORT}")
    print(f"  Attack Type: Brute-force authentication")
    print("=" * 60)
    print()

def attempt_login(username, password, attempt_num):
    """Attempt to connect and login to target service"""
    try:
        print(f"[Attempt {attempt_num}] Trying {username}:{password}...", end=" ")
        
        # Create socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((TARGET_IP, TARGET_PORT))
        
        # Receive banner/prompt
        response = sock.recv(2048).decode('utf-8', errors='ignore')
        
        # Send credentials (even though it's fake)
        sock.sendall(f"{username}\n{password}\n".encode())
        
        # Try to receive response
        time.sleep(1)
        try:
            response2 = sock.recv(2048).decode('utf-8', errors='ignore')
            print(f"[RESPONSE] {response2.strip()[:50]}...")
        except:
            print("[TIMEOUT] No response")
        
        sock.close()
        
        # Print what we observed
        if "Login incorrect" in response or "Login incorrect" in (response2 if 'response2' in locals() else ''):
            print("    → Status: LOGIN REJECTED (as expected)")
        elif "Authenticating" in response or "Loading" in response:
            print("    → Status: SYSTEM STALLING")
        elif "busy" in response.lower():
            print("    → Status: SERVICE UNAVAILABLE")
        else:
            print("    → Status: UNKNOWN RESPONSE")
            
    except socket.timeout:
        print("[ERROR] Connection timeout")
    except ConnectionRefusedError:
        print("[ERROR] Connection refused - is deception.py running?")
        print("        Run: sudo venv/bin/python deception.py")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}")

def main():
    print_banner()
    
    print("[ATTACKER] Starting automated brute-force attack...")
    print("[ATTACKER] This simulates how Mirai botnet scans IoT devices\n")
    
    time.sleep(2)
    
    for i, (username, password) in enumerate(CREDENTIALS, 1):
        attempt_login(username, password, i)
        time.sleep(2)  # Delay between attempts
        
        if i < len(CREDENTIALS):
            print()  # Spacing between attempts
    
    print("\n" + "=" * 60)
    print("  ATTACK SIMULATION COMPLETE")
    print("=" * 60)
    print("\n[ATTACKER] In a real attack, the bot would:")
    print("  1. Move to next target if login fails")
    print("  2. Try to compromise the device if successful")
    print("  3. Turn device into part of botnet")
    print("\n[SENTINEL] Your honeypot successfully:")
    print("  ✅ Wasted attacker time (5+ attempts)")
    print("  ✅ Gathered intelligence (credentials tried)")
    print("  ✅ Protected real device (never exposed)")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[ATTACKER] Simulation interrupted by user")
        sys.exit(0)
