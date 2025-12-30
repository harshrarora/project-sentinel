#!/usr/bin/env python3
import socket
import datetime
import json
import os
import time

PORT = 2323
EVENT_FILE = "events.json"

STATES = ["ENGAGING", "STALLING", "CONTAINED"]


def load_events():
    if not os.path.exists(EVENT_FILE):
        return []
    with open(EVENT_FILE, "r") as f:
        return json.load(f)


def save_event(event):
    events = load_events()
    events.append(event)
    with open(EVENT_FILE, "w") as f:
        json.dump(events, f, indent=2)


def handle_client(conn, addr, state):
    if state == "ENGAGING":
        conn.sendall(b"login: password:\nLogin incorrect\n")
    elif state == "STALLING":
        conn.sendall(b"Authenticating...\nLoading configuration...\n")
        time.sleep(2)
    elif state == "CONTAINED":
        conn.sendall(b"System busy. Try again later.\n")

    conn.close()


def main():
    print("Sentinel Deception Module started")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", PORT))
    server.listen(5)

    idx = 0

    while True:
        conn, addr = server.accept()
        state = STATES[idx % len(STATES)]

        event = {
            "timestamp": str(datetime.datetime.now()),
            "source_ip": addr[0],
            "port": PORT,
            "state": state,
            "action": "DECEPTION_ENGAGED"
        }

        save_event(event)
        handle_client(conn, addr, state)
        idx += 1


if __name__ == "__main__":
    main()
