#!/usr/bin/env python3
import json
import subprocess
import datetime
import os
import signal

SCAN_FILE = "scan.json"
DECISION_FILE = "decisions.json"
DECEPTION_SCRIPT = "deception.py"


def decide(devices):
    decisions = []

    for d in devices:
        decisions.append({
            "ip": d["ip"],
            "action": "DECEIVE",
            "reason": "Demo override: showcasing autonomous deception capability"
        })

    return decisions


def launch_deception():
    print("[AGENT] Launching deception module...")
    subprocess.Popen(
        ["sudo", "venv/bin/python", DECEPTION_SCRIPT],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid
    )


def main():
    with open(SCAN_FILE, "r") as f:
        scan = json.load(f)

    decisions = decide(scan["devices"])

    output = {
        "timestamp": str(datetime.datetime.now()),
        "decisions": decisions
    }

    with open(DECISION_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(json.dumps(output, indent=2))

    if any(d["action"] == "DECEIVE" for d in decisions):
        launch_deception()


if __name__ == "__main__":
    main()
