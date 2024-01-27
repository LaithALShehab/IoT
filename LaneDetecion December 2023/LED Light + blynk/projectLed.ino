#define BLYNK_PRINT Serial
#define BLYNK_TEMPLATE_ID   "TMPL6f0kSYL8c"  // Replace with your Blynk template ID
#define BLYNK_TEMPLATE_NAME "first project"  // Replace with your Blynk template name
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

#define BLYNK_AUTH_TOKEN "arJTCm_3bxMRIaFjQaX2nuqGBQVUwuSt" // Enter your Blynk auth token

char auth[] = BLYNK_AUTH_TOKEN;
char ssid[] = " ";  // Enter your WIFI name
char pass[] = " ";  // Enter your WIFI password

// Get the button value
BLYNK_WRITE(V0) {
  digitalWrite(D0, param.asInt());
}

void setup() {
  // Set the LED pin as an output pin
  pinMode(D0, OUTPUT);
  // Initialize the Blynk library
  Blynk.begin(auth, ssid, pass, "blynk.cloud", 80);
}

void loop() {
  // Run the Blynk library
  Blynk.run();
}
