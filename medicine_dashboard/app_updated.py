import serial
import time
from datetime import datetime
from flask import Flask, render_template, jsonify, request
import threading
import json
from pathlib import Path

app = Flask(__name__)

class MedicineReminderSystem:
    def __init__(self):
        self.ser = None
        self.running = True
        self.alarm_active = False
        self.medicine_times = ["09:00", "14:00", "22:10"]
        self.config_file = "config.json"
        self.last_alarm_time = None
        
        # Load config
        self.load_config()
        
        # Connect to Arduino
        self.connect_arduino()
    
    def load_config(self):
        """Load configuration from file"""
        if Path(self.config_file).exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.medicine_times = config.get('medicine_times', self.medicine_times)
            except:
                pass
    
    def save_config(self):
        """Save configuration to file"""
        config = {'medicine_times': self.medicine_times}
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def connect_arduino(self):
        """Connect to Arduino via COM4"""
        try:
            self.ser = serial.Serial('COM4', 9600, timeout=1)
            time.sleep(2)
            print(f"✓ Connected to COM4 at {datetime.now()}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to Arduino: {e}")
            self.ser = None
            return False
    
    def send_command(self, command):
        """Send command to Arduino"""
        if self.ser and self.ser.is_open:
            try:
                self.ser.write((command + '\n').encode())
                return True
            except:
                return False
        return False
    
    def read_arduino_response(self):
        """Read response from Arduino"""
        if self.ser and self.ser.is_open:
            try:
                if self.ser.in_waiting:
                    response = self.ser.readline().decode().strip()
                    return response
            except:
                pass
        return None
    
    def trigger_alarm(self, medicine_name="Medicine"):
        """Trigger alarm - buzzer and LED blink"""
        if self.alarm_active:
            return False
        
        self.alarm_active = True
        self.last_alarm_time = datetime.now()
        
        print(f"🚨 ALARM TRIGGERED for {medicine_name} at {self.last_alarm_time}")
        
        # Send ALARM command to Arduino
        self.send_command("ALARM")
        
        return True
    
    def stop_alarm(self):
        """Stop alarm"""
        self.alarm_active = False
        self.send_command("STOP")
        print(f"✓ Alarm stopped at {datetime.now()}")
    
    def check_button_press(self):
        """Check if hardware button was pressed"""
        response = self.read_arduino_response()
        if response:
            print(f"Arduino: {response}")
            if "BUTTON_PRESSED_STOP" in response:
                if self.alarm_active:
                    self.stop_alarm()
                    print("⚠️ ALARM STOPPED BY HARDWARE BUTTON!")
                    return True
        return False
    
    def check_time_and_alarm(self):
        """Check if it's time for medicine (runs in background)"""
        last_checked = None
        
        while self.running:
            try:
                # Check for button press
                self.check_button_press()
                
                current_time = datetime.now().strftime("%H:%M")
                
                # Check if current time matches any medicine time
                if current_time in self.medicine_times and current_time != last_checked:
                    last_checked = current_time
                    self.trigger_alarm(f"Medicine at {current_time}")
                
                # Reset last_checked when time changes
                if current_time not in self.medicine_times:
                    last_checked = None
                
                time.sleep(1)
            except Exception as e:
                print(f"Error in time checker: {e}")
    
    def get_status(self):
        """Get current system status"""
        return {
            'alarm_active': self.alarm_active,
            'connected': self.ser is not None and self.ser.is_open,
            'medicine_times': self.medicine_times,
            'current_time': datetime.now().strftime("%H:%M:%S"),
            'last_alarm': self.last_alarm_time.strftime("%Y-%m-%d %H:%M:%S") if self.last_alarm_time else None
        }

# Initialize system
reminder_system = MedicineReminderSystem()

# Start background thread for time checking
def start_background_checker():
    checker_thread = threading.Thread(target=reminder_system.check_time_and_alarm, daemon=True)
    checker_thread.start()

start_background_checker()

# ==================== Flask Routes ====================

@app.route('/')
def index():
    """Serve the web interface"""
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status"""
    return jsonify(reminder_system.get_status())

@app.route('/api/alarm/trigger', methods=['POST'])
def trigger_alarm_manual():
    """Manually trigger alarm"""
    data = request.json
    medicine_name = data.get('medicine', 'Medicine')
    
    if reminder_system.trigger_alarm(medicine_name):
        return jsonify({'status': 'success', 'message': 'Alarm triggered'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Alarm already active'}), 400

@app.route('/api/alarm/stop', methods=['POST'])
def stop_alarm_endpoint():
    """Stop the alarm (SOFTWARE BUTTON)"""
    reminder_system.stop_alarm()
    return jsonify({'status': 'success', 'message': 'Alarm stopped by software button'}), 200

@app.route('/api/config/medicine-times', methods=['GET', 'POST'])
def medicine_times():
    """Get or update medicine times"""
    if request.method == 'POST':
        data = request.json
        reminder_system.medicine_times = data.get('times', [])
        reminder_system.save_config()
        return jsonify({'status': 'success', 'times': reminder_system.medicine_times}), 200
    
    return jsonify({'times': reminder_system.medicine_times}), 200

@app.route('/api/test/arduino', methods=['GET'])
def test_arduino():
    """Test Arduino connection"""
    if reminder_system.connect_arduino():
        return jsonify({'status': 'success', 'message': 'Arduino connected'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to connect Arduino'}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    print("=" * 70)
    print("Smart Medicine Reminder System - Web Interface")
    print("WITH HARDWARE BUTTON SUPPORT (Software + Hardware Stop)")
    print("=" * 70)
    print("Starting Flask server...")
    print("Open http://localhost:5000 in your browser")
    print("=" * 70)
    print()
    print("Controls:")
    print("  🔴 SOFTWARE STOP: Web dashboard 'Stop Alarm' button")
    print("  🔘 HARDWARE STOP: Press physical button on breadboard")
    print()
    print("=" * 70)
    
    # Run Flask app
    app.run(debug=True, host='localhost', port=5000, use_reloader=False)
