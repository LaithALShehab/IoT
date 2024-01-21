int GREEN_LED = 9;
int RED_LED = 10;
int BUZZER_PIN = 8;

void setup() {
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  Serial.begin(9600);
}
void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    
    if (input.equals("no_mask"))
    {
            // Person is not wearing a mask
      digitalWrite(GREEN_LED, LOW);
      digitalWrite(RED_LED, HIGH);
      tone(BUZZER_PIN, 1500, 500);  // Play a 1500 Hz tone for 500 milliseconds
      delay(800);  // Add a delay to control the sound duration
      noTone(BUZZER_PIN); // Play the warning sound
      digitalWrite(RED_LED, LOW);

    } 
    else if (input.equals("mask")) {
      // Person is wearing a mask
      digitalWrite(GREEN_LED, HIGH);
      digitalWrite(RED_LED, LOW);
      tone(BUZZER_PIN, 1000, 500);  // Play a 1000 Hz tone for 500 milliseconds
      delay(800);  // Add a delay to control the sound duration
      noTone(BUZZER_PIN);  // Turn off the buzzer
      digitalWrite(GREEN_LED, LOW);
    } 
    
  }
}