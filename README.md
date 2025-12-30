# Project Sentinel

**Agentic AI-Powered IoT Security Through Risk-Weighted Stateful Deception**

> Protecting home IoT devices through intelligent deception, not blind blocking.

## The Problem

Modern homes contain 10-25 IoT devices that are fundamentally insecure:
- Can't be patched or updated
- Expose vulnerable services (Telnet, SSH, HTTP)
- Can't run endpoint security software
- Targeted by automated botnets (Mirai-style attacks)
Traditional firewalls are reactive and complex for home users

## The Solution

Project Sentinel is an autonomous AI agent that:
- **Discovers** IoT devices automatically via ARP scanning
- **Reasons** about threats using explainable decision logic
- **Deceives** attackers with stateful honeypots (Digital Twins)
- **Contains** threats without disrupting legitimate traffic

### Key Innovation: Risk-Weighted Stateful Deception

Unlike static honeypots, Sentinel:
- Deploys deception **only when needed** based on risk assessment
- Maintains **per-attacker state** (ENGAGING → STALLING → CONTAINED)
- Makes **explainable decisions** with transparent reasoning

## Architecture
```
┌─────────────────┐
│ PERCEPTION      │  Network discovery & risk profiling
│ (scanner.py)    │
└────────┬────────┘
         ↓
┌─────────────────┐
│ REASONING       │  Agentic decision engine
│ (agent.py)      │
└────────┬────────┘
         ↓
┌─────────────────┐
│ DECEPTION       │  Stateful Digital Twins
│ (deception.py)  │
└─────────────────┘
```

## Quick Start

### Prerequisites
- Python 3.9+
- Linux/Mac (for ARP scanning)
- Root/sudo access

### Installation
```bash
# Clone repository
git clone https://github.com/harshrarora/project-sentinel.git
cd project-sentinel

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run Demo
```bash
# Automated demo
./run_demo.sh

# Manual steps
sudo venv/bin/python scanner.py      # Discover devices
sudo venv/bin/python agent.py        # Agent reasoning
sudo venv/bin/python deception.py &  # Deploy honeypot
streamlit run dashboard.py           # View dashboard
```

### Simulate Attack
```bash
# In another terminal
python attack_sim.py
```

## Demo Results

- **Detection Time:** < 30 seconds
- **Containment Time:** < 1 minute
- **False Positives:** 0%
- **Real Device Compromised:** NO

## Technology Stack

- **Python**
- **scapy (ARP scanning)**
- **Streamlit dashboard**
- **socket programming** 
- **JSON-based inter-module communication**

## Future Roadmap

### Phase 2
- Real firewall integration (iptables)
- VLAN-based device isolation
- Multi-protocol honeypots (SSH, HTTP)
- Machine learning anomaly detection

### Phase 3
- Raspberry Pi appliance
- Mobile app for alerts
- Threat intelligence sharing
- Commercial deployment


## Author

**Harsh Rakesh Arora**
- solo hackathon project
- Built for: eRaksha Hackathon 2026
- Contact: harshrakesharora@gmail.com
