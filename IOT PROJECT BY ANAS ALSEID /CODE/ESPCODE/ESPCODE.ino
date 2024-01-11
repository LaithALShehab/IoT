#define BLYNK_TEMPLATE_ID "TMPL6UO0OPJzF"
#define BLYNK_TEMPLATE_NAME "Quickstart Template"

#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

char ssid[] = "M7md's room";
char pass[] = "Musallam123";
char auth[] = "Gwpxx9uoxznU8ruTyAu0Cml-eMG492JE";

BlynkTimer timer;

void sendSensorData() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    int firstComma = data.indexOf(',');
    int secondComma = data.indexOf(',', firstComma + 1);
    int thirdComma = data.indexOf(',', secondComma + 1);
    int fourthComma = data.indexOf(',', thirdComma + 1);
    int fifthComma = data.indexOf(',', fourthComma + 1);

    int waterLevel = data.substring(0, firstComma).toInt();
    float pH = data.substring(firstComma + 1, secondComma).toFloat() / 1024.0 * 14.0;
    float voltage = data.substring(secondComma + 1, thirdComma).toFloat() * (5.0 / 1023.0);
    float current = data.substring(thirdComma + 1, fourthComma).toFloat() * (5.0 / 1023.0);
    int motion = data.substring(fourthComma + 1, fifthComma).toInt();
    float waterTemp = data.substring(fifthComma + 1).toFloat();

    Blynk.virtualWrite(V1, waterLevel);
    Blynk.virtualWrite(V2, pH);
    Blynk.virtualWrite(V3, voltage);
    Blynk.virtualWrite(V4, current);
    Blynk.virtualWrite(V5, motion);
    Blynk.virtualWrite(V6, waterTemp); // Send water temperature to virtual pin V6
  }
}

void setup() {
  Serial.begin(9600);
  Blynk.begin(auth, ssid, pass);
  timer.setInterval(1000L, sendSensorData);
}

void loop() {
  Blynk.run();
  timer.run();
}
