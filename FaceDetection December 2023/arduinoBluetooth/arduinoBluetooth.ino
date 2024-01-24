#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 20, 4); 
String receivedData = ""; 
int redLedPin = 8;
int greenLedPin = 9;
int buzzerPin = 10; 
const int relayPin = 7; 

void setup() {
  Serial.begin(9600); // Initialize serial communication
  lcd.init();         // initialize the lcd
  lcd.backlight();    // Turn on the LCD screen backlight
  pinMode(redLedPin, OUTPUT); // Set red LED pin as output
  pinMode(greenLedPin, OUTPUT); // Set green LED pin as output
  pinMode(buzzerPin, OUTPUT); // Set buzzer pin as output
  pinMode(relayPin, OUTPUT); // Set relay pin as output
  digitalWrite(redLedPin, LOW); // Initially, turn off the red LED
  digitalWrite(greenLedPin, LOW); // Initially, turn off the green LED
  digitalWrite(buzzerPin, LOW); // Initially, turn off the buzzer
  digitalWrite(relayPin, HIGH); // Initially, keep the relay off
}

void loop() {
  if (Serial.available() > 0) { // Check if data is available to read
    receivedData = Serial.readString(); // Read the received data
    lcd.clear(); // Clear the LCD display

    if (receivedData.startsWith("Unauthorized")) {
      lcd.setCursor(0, 0);
      lcd.print("Unauthorized User");
      digitalWrite(redLedPin, HIGH); // Turn on the red LED
      digitalWrite(greenLedPin, LOW); // Turn off the green LED
      tone(buzzerPin, 1000, 1000); // Play a 1-second tone for unauthorized
      digitalWrite(relayPin, HIGH); // Deactivate the relay for unauthorized
      delay(1000); // Buzzer duration
      noTone(buzzerPin); // Stop the buzzer sound
      
    } else {
      lcd.setCursor(0, 0);
      lcd.print("Welcome");
      lcd.setCursor(0, 1);
      // Adjust substring boundaries to avoid the last character
      lcd.print(receivedData.substring(0, receivedData.length())); 
      digitalWrite(redLedPin, LOW); // Turn off the red LED
      digitalWrite(greenLedPin, HIGH); // Turn on the green LED
      tone(buzzerPin, 2000, 200); // Play a different tone for authorized
      digitalWrite(relayPin, LOW); // Activate the relay for authorized
      delay(5000); // Wait for 5 seconds
      digitalWrite(greenLedPin, LOW); // Turn off the green LED
      digitalWrite(relayPin, HIGH); // Deactivate the relay after 5 seconds
      noTone(buzzerPin); // Stop the buzzer sound
      delay(2000); // Wait for an additional 2 seconds (adjust as needed)
      lcd.clear(); // Clear the LCD display again
    }
  }
  delay(1000); 
}
