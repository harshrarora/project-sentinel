#!/bin/bash

echo "========================================="
echo "   PROJECT SENTINEL - LIVE DEMO"
echo "========================================="
echo ""

# Check if running in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not activated"
    echo "   Run: source venv/bin/activate"
    exit 1
fi

# Step 1: Network Discovery
echo "[1/4] 🔍 Running network discovery..."
echo "      Scanning local network for IoT devices..."
sudo venv/bin/python scanner.py > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "      ✅ Discovery complete"
    # Show discovered devices
    DEVICE_COUNT=$(cat scan.json | grep -o '"ip"' | wc -l)
    echo "      📡 Found $DEVICE_COUNT device(s)"
else
    echo "      ❌ Scanner failed"
    exit 1
fi

sleep 2
echo ""

# Step 2: Agent Decision Making
echo "[2/4] 🧠 Agent analyzing threats..."
echo "      Assessing risk and making decisions..."
sudo venv/bin/python agent.py > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "      ✅ Agent decisions made"
    # Check if deception needed
    DECEIVE_COUNT=$(cat decisions.json | grep -o '"DECEIVE"' | wc -l)
    if [ $DECEIVE_COUNT -gt 0 ]; then
        echo "      🔴 High-risk devices detected: $DECEIVE_COUNT"
        echo "      📋 Deploying countermeasures..."
    else
        echo "      🟢 No threats detected"
    fi
else
    echo "      ❌ Agent failed"
    exit 1
fi

sleep 2
echo ""

# Step 3: Deploy Deception Layer
echo "[3/4] 🪤 Deploying Digital Twins..."
echo "      Starting autonomous deception services..."

# Check if deception already running
if sudo ss -lntp 2>/dev/null | grep -q ":2323"; then
    echo "      ⚠️  Deception already running on port 2323"
    echo "      ℹ️  Skipping deployment"
else
    sudo venv/bin/python deception.py > /dev/null 2>&1 &
    DECEPTION_PID=$!
    sleep 2
    
    # Verify it started
    if sudo ss -lntp 2>/dev/null | grep -q ":2323"; then
        echo "      ✅ Ghost service active on port 2323"
        echo "      🎭 Digital Twin ready to engage threats"
    else
        echo "      ❌ Failed to start deception service"
        exit 1
    fi
fi

sleep 1
echo ""

# Step 4: Launch Dashboard
echo "[4/4] 📊 Starting dashboard..."
echo "      Launching real-time monitoring interface..."

# Kill existing Streamlit instances
pkill -f streamlit 2>/dev/null

# Start dashboard in background
streamlit run dashboard.py > /dev/null 2>&1 &
DASHBOARD_PID=$!

sleep 3

echo "      ✅ Dashboard launched"
echo ""

# Final Status
echo "========================================="
echo "   ✅ SENTINEL OPERATIONAL"
echo "========================================="
echo ""
echo "📊 Dashboard:    http://localhost:8501"
echo "🪤 Ghost Service: Port 2323 (Active)"
echo "📡 Monitoring:   $DEVICE_COUNT device(s)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  DEMO INSTRUCTIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  Open dashboard in browser:"
echo "    → http://localhost:8501"
echo ""
echo "2️⃣  Simulate attack in new terminal:"
echo "    → python attack_sim.py"
echo ""
echo "3️⃣  OR manually test with telnet:"
echo "    → telnet 127.0.0.1 2323"
echo ""
echo "4️⃣  Watch dashboard update in real-time!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping Sentinel services..."
    
    # Kill deception service
    if [ ! -z "$DECEPTION_PID" ]; then
        sudo kill $DECEPTION_PID 2>/dev/null
    fi
    
    # Kill dashboard
    if [ ! -z "$DASHBOARD_PID" ]; then
        kill $DASHBOARD_PID 2>/dev/null
    fi
    
    # Kill any remaining processes
    pkill -f streamlit 2>/dev/null
    sudo pkill -f deception.py 2>/dev/null
    
    echo "✅ All services stopped"
    echo "👋 Sentinel offline"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Keep script running
while true; do
    sleep 1
done
