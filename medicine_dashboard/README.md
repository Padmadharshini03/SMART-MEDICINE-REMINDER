╔══════════════════════════════════════════════════════════════════════════════╗
║           SMART MEDICINE REMINDER SYSTEM - SETUP GUIDE                       ║
║                     Arduino + Web Interface + Windows                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 SYSTEM OVERVIEW
==================
This system consists of:
1. Arduino (Buzzer + LED control)
2. Python Flask Web Server
3. Beautiful Web Dashboard
4. Automatic alarm triggers at scheduled times
5. Manual alarm triggers via web interface

⚙️ HARDWARE SETUP (Arduino Wiring)
==================================

Components Needed:
  - Arduino Uno or Nano
  - Buzzer (Active or Passive)
  - LED (any color)
  - 220Ω Resistor (for LED)
  - USB Cable to connect Arduino to PC
  - Breadboard & Jumper Wires

Wiring Diagram:
  Buzzer:
    - Positive → Arduino Pin 9 (PWM)
    - Negative → Arduino GND

  LED:
    - Positive → Arduino Pin 13 (through 220Ω resistor)
    - Negative → Arduino GND

  USB Connection:
    - Connect Arduino to PC via USB
    - Driver will auto-install (Windows)


📝 STEP 1: Upload Arduino Code
==============================

Option A: Using Arduino IDE (Recommended)
  1. Download Arduino IDE from https://www.arduino.cc/en/software
  2. Install and open Arduino IDE
  3. Go to Tools → Board → Select "Arduino Uno" (or your board)
  4. Go to Tools → Port → Select COM port (e.g., COM4)
  5. Copy the code from "medicine_reminder_arduino.ino"
  6. Paste into Arduino IDE
  7. Click Upload (or Ctrl+U)
  8. Wait for "Done uploading" message
  9. Open Serial Monitor (Tools → Serial Monitor)
  10. Set Baud Rate to 9600
  11. You should see "Arduino Ready"

Option B: Using Arduino Web Editor
  1. Go to https://create.arduino.cc/
  2. Create account if needed
  3. Create new sketch
  4. Paste code from "medicine_reminder_arduino.ino"
  5. Click Upload


🐍 STEP 2: Install Python Dependencies
=======================================

Windows:
  1. Open Command Prompt (Windows + R → type "cmd")
  2. Navigate to project folder:
     cd C:\path\to\medicine_reminder

  3. Install Python packages:
     pip install -r requirements.txt
  
  Alternatively, install manually:
     pip install Flask==2.3.2
     pip install pyserial==3.5
     pip install Werkzeug==2.3.6


🚀 STEP 3: Run the Web Application
===================================

  1. Open Command Prompt
  2. Navigate to project folder:
     cd C:\path\to\medicine_reminder

  3. Run the Flask app:
     python app.py

  4. You should see:
     ============================================================
     Smart Medicine Reminder System - Web Interface
     ============================================================
     Starting Flask server...
     Open http://localhost:5000 in your browser
     ============================================================

  5. Open your browser and go to:
     http://localhost:5000

  6. The dashboard should load with all controls!


💻 WEB INTERFACE FEATURES
=========================

✓ System Status Panel
  - Arduino connection status
  - Alarm status (Active/Idle)
  - Current time display

✓ Medicine Schedule
  - View all medicine times
  - Add new medicine times
  - Remove existing times
  - Times are saved automatically

✓ Controls
  - Manual alarm trigger button (TEST MODE)
  - Stop alarm button
  - Test Arduino connection button
  - Refresh page button

✓ Last Alarm Display
  - Shows when the last alarm was triggered


🔔 HOW IT WORKS
===============

Automatic Mode:
  1. System checks time every second
  2. When current time matches a medicine time:
     a. Sends "ALARM" command to Arduino
     b. Arduino triggers buzzer (beeps 3x)
     c. Arduino LED blinks rapidly
     d. Web interface shows alarm as ACTIVE
     e. Browser shows alert notification

Manual Testing:
  1. Click "TRIGGER ALARM NOW" button on web interface
  2. Arduino receives command and activates alarm
  3. Buzzer beeps and LED blinks
  4. You can test without waiting for scheduled time

Stopping:
  1. Click "Stop Alarm" button
  2. Sends "STOP" command to Arduino
  3. Buzzer and LED turn off immediately
  4. Status updates to "Idle"


⏰ SETTING UP MEDICINE TIMES
=============================

From Web Interface:
  1. Go to "Medicine Schedule" section
  2. Select time using time picker (HH:MM format)
  3. Click "Add Time"
  4. Time appears as a badge
  5. Remove times by clicking the ✕ button

Example Schedule:
  ⏰ 09:00  (Morning)
  ⏰ 14:00  (Afternoon)
  ⏰ 22:10  (Evening)


🔧 TROUBLESHOOTING
==================

Problem: Arduino not connecting
  Solution:
    1. Check USB cable connection
    2. Verify COM port number (Device Manager → Ports)
    3. Install Arduino drivers if needed
    4. Try different USB port
    5. Restart Arduino: unplug for 5 seconds, plug back in
    6. Check if port matches in app.py (line 33: 'COM4')

Problem: Buzzer not making sound
  Solution:
    1. Check wiring - buzzer positive to Pin 9
    2. Test with Arduino IDE Serial Monitor:
       - Type "ALARM" and send
       - Buzzer should beep
    3. Verify buzzer is rated for 5V
    4. Try swapping buzzer wires if it's not polarized

Problem: LED not blinking
  Solution:
    1. Check LED polarity (long leg = positive)
    2. Verify 220Ω resistor is connected correctly
    3. Check Pin 13 on Arduino
    4. Test LED directly on 5V (briefly)

Problem: Web interface won't open
  Solution:
    1. Ensure Flask is running (python app.py)
    2. Try http://localhost:5000 or http://127.0.0.1:5000
    3. Check if port 5000 is available:
       - Windows: netstat -ano | findstr :5000
       - If in use, change port in app.py line 155: port=5001

Problem: Medicine times not saving
  Solution:
    1. Make sure config.json file can be created
    2. Check folder permissions
    3. Try restarting Flask app


📱 ACCESSING FROM OTHER DEVICES
================================

Same WiFi Network:
  1. Find your PC's IP address:
     - Windows: ipconfig (look for IPv4 Address)
     - Example: 192.168.1.100
  
  2. On other device, open browser:
     http://192.168.1.100:5000

  3. Enter your medicine times

Note: Arduino must be connected to the PC that runs Flask


🔐 KEEPING SYSTEM RUNNING 24/7 (Windows)
==========================================

Option 1: Using Task Scheduler
  1. Create file "run_medicine.bat":
     @echo off
     cd C:\path\to\medicine_reminder
     python app.py

  2. Open Task Scheduler
  3. Create Basic Task
  4. Name: "Medicine Reminder"
  5. Trigger: "At startup"
  6. Action: "Start a program"
  7. Program: C:\path\to\run_medicine.bat
  8. Check "Run with highest privileges"

Option 2: Using NSSM (Non-Sucking Service Manager)
  1. Download NSSM from https://nssm.cc/download
  2. Extract nssm.exe
  3. Open Command Prompt as Administrator
  4. Run:
     nssm install MedicineReminder python C:\path\to\app.py
     nssm start MedicineReminder
  5. Stop service:
     nssm stop MedicineReminder


📊 FILE STRUCTURE
=================

medicine_reminder/
├── app.py                          (Main Flask application)
├── requirements.txt                (Python dependencies)
├── medicine_reminder_arduino.ino   (Arduino sketch)
├── config.json                     (Saved medicine times)
└── templates/
    └── index.html                  (Web dashboard)


🔄 UPDATING MEDICINE TIMES
===========================

Times are stored in config.json
Format: {"medicine_times": ["09:00", "14:00", "22:10"]}

You can:
  - Edit via web interface (recommended)
  - Edit config.json directly (restart Flask after)
  - Add/remove times anytime


📞 SUPPORT TIPS
===============

For debugging:
  1. Check console output when Flask is running
  2. Open browser console (F12) for JavaScript errors
  3. Test Arduino directly with Serial Monitor
  4. Try triggering alarm manually first

If alarm doesn't trigger at scheduled time:
  1. Verify medicine time format is correct (HH:MM)
  2. Check system time on PC is correct
  3. Keep Flask running in background
  4. Check Arduino is still connected


🎯 QUICK START CHECKLIST
========================

□ Arduino wired: Buzzer to Pin 9, LED to Pin 13
□ Arduino code uploaded and tested
□ Arduino shows "Arduino Ready" in Serial Monitor
□ Python installed (python --version)
□ Flask and pyserial installed (pip list)
□ Flask app running (python app.py)
□ Web interface opens at http://localhost:5000
□ Arduino status shows "Connected"
□ Test alarm works (manual trigger)
□ Medicine times added to schedule
□ System ready for 24/7 operation!


═══════════════════════════════════════════════════════════════════════════════
Enjoy your automated medicine reminder system! 💊
═══════════════════════════════════════════════════════════════════════════════
