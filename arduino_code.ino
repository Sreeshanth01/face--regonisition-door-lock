#include <Servo.h>

const int RED_PIN = 5;
const int BUZZER_PIN = 6;
const int SERVO_PIN = 13;

Servo doorServo;

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  doorServo.attach(SERVO_PIN);
  doorServo.write(0); // Start locked

  // Default state: locked (red LED ON)
  digitalWrite(RED_PIN, HIGH);

  Serial.begin(115200);
  Serial.println("System ready. Type ACCEPT or REJECT to test.");
}

// ---- Tunes ----
// Authorized (Accepted)
int acceptNotes[] = {659, 784, 988, 784};
int acceptDur[]   = {150, 150, 180, 150};
int acceptLen = sizeof(acceptNotes) / sizeof(acceptNotes[0]);

// Unauthorized (Rejected)
int rejectNotes[] = {330, 262, 196};
int rejectDur[]   = {200, 200, 300};
int rejectLen = sizeof(rejectNotes) / sizeof(rejectNotes[0]);

// Play tune helper
void playTune(int notes[], int durs[], int len) {
  for (int i = 0; i < len; i++) {
    tone(BUZZER_PIN, notes[i]);
    delay(durs[i]);
    noTone(BUZZER_PIN);
    delay(40);
  }
}

// --- Authorized Face Detected ---
void acceptedFace() {
  Serial.println("Authorized face detected.");
  digitalWrite(RED_PIN, LOW);    // Turn OFF red LED
  playTune(acceptNotes, acceptDur, acceptLen); // Play success tone

  doorServo.write(90);           // Unlock (rotate 90°)
  delay(3000);                   // Wait 3 seconds
  doorServo.write(0);            // Lock again

  digitalWrite(RED_PIN, HIGH);   // Turn ON red LED again
}

// --- Unauthorized Face Detected ---
void rejectedFace() {
  Serial.println("Unauthorized face detected.");
  digitalWrite(RED_PIN, HIGH);   // Keep red ON
  playTune(rejectNotes, rejectDur, rejectLen); // Play reject tone
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd.equalsIgnoreCase("ACCEPT") || cmd.equalsIgnoreCase("OPEN") || cmd == "1") {
      acceptedFace();
    } 
    else if (cmd.equalsIgnoreCase("REJECT") || cmd.equalsIgnoreCase("DENY") || cmd == "0") {
      rejectedFace();
    } 
    else {
      Serial.println("Invalid command. Type ACCEPT or REJECT.");
    }
  }
}
