/*
  Smart Medicine Reminder System - Arduino Code
  WITH HARDWARE STOP BUTTON
  
  Pin 8:  LED (blinks when alarm)
  Pin 9:  Buzzer (beeps when alarm)
  Pin 7:  Stop Button (press to stop alarm immediately)
  A4, A5: RTC (optional - not used in this code)
  
  Features:
  - Receives commands from Python via Serial
  - Controls Buzzer and LED based on commands
  - Hardware button stops alarm immediately without waiting for Python
  - Dual control: Software (Python) + Hardware (Button)
*/

#define BUZZER_PIN 9
#define LED_PIN 8
#define BUTTON_PIN 7

bool alarmActive = false;
unsigned long lastBlinkTime = 0;
const int BLINK_INTERVAL = 300; // milliseconds
bool ledState = false;

void setup() {
  Serial.begin(9600);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);  // Button input (with pull-up resistor)
  
  // Initialize all off
  digitalWrite(BUZZER_PIN, LOW);
  digitalWrite(LED_PIN, LOW);
  
  Serial.println("Arduino Ready");
  delay(500);
}

void loop() {
  // ===== CHECK HARDWARE BUTTON FIRST =====
  // This runs every loop - fastest response
  if (digitalRead(BUTTON_PIN) == LOW) {
    // Button is pressed (LOW because of pull-up resistor)
    if (alarmActive) {
      stopAlarm();
      Serial.println("BUTTON_PRESSED_STOP");
      delay(500);  // Debounce delay to prevent false triggers
    }
  }
  
  // ===== CHECK SERIAL COMMANDS FROM PYTHON =====
  // Commands: ALARM, STOP, STATUS
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    processCommand(command);
  }
  
  // ===== HANDLE LED BLINKING DURING ALARM =====
  // LED blinks continuously while alarm is active
  if (alarmActive) {
    unsigned long currentTime = millis();
    if (currentTime - lastBlinkTime >= BLINK_INTERVAL) {
      lastBlinkTime = currentTime;
      ledState = !ledState;
      digitalWrite(LED_PIN, ledState ? HIGH : LOW);
      
      // Also buzz on each blink (buzzer pattern)
      digitalWrite(BUZZER_PIN, HIGH);
      delay(100);
      digitalWrite(BUZZER_PIN, LOW);
    }
  }
}

void processCommand(String cmd) {
  // Process commands from Python
  
  if (cmd == "ALARM") {
    // Python says: START ALARM
    activateAlarm();
    Serial.println("ALARM_ACTIVATED");
  }
  else if (cmd == "STOP") {
    // Python says: STOP ALARM (SOFTWARE BUTTON)
    stopAlarm();
    Serial.println("ALARM_STOPPED_SOFTWARE");
  }
  else if (cmd == "STATUS") {
    // Python asks: What's your status?
    if (alarmActive) {
      Serial.println("STATUS:ALARM_ACTIVE");
    } else {
      Serial.println("STATUS:IDLE");
    }
  }
}

void activateAlarm() {
  // Turn on alarm: beep buzzer 3 times + blink LED
  alarmActive = true;
  
  // Initial strong buzzer and LED signals (3 beeps)
  for (int i = 0; i < 3; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    
    digitalWrite(BUZZER_PIN, LOW);
    digitalWrite(LED_PIN, LOW);
    delay(200);
  }
  
  // Set up for continuous LED blinking in main loop
  lastBlinkTime = millis();
  ledState = true;
}

void stopAlarm() {
  // Turn off alarm: stop buzzer + stop LED
  alarmActive = false;
  digitalWrite(BUZZER_PIN, LOW);
  digitalWrite(LED_PIN, LOW);
  ledState = false;
}
