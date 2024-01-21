#include <SoftwareSerial.h>
#include <OneWire.h>
#include <DallasTemperature.h>

SoftwareSerial EspSerial(18, 19); // RX, TX

// DS18B20 Sensor on pin 23
const int oneWireBus = 23;        
OneWire oneWire(oneWireBus);
DallasTemperature sensors(&oneWire);

// Other sensor pins
const int waterLevelSensorPin = A0;
const int pHsensorPin = A1;
const int voltageSensorPin = A2;
const int currentSensorPin = A3;
const int motionSensorPin = 4;
const int chlorinePumpPin = 22;

void setup() {
  EspSerial.begin(9600);
  sensors.begin(); // Start the DS18B20 sensor

  pinMode(waterLevelSensorPin, INPUT);
  pinMode(pHsensorPin, INPUT);
  pinMode(voltageSensorPin, INPUT);
  pinMode(currentSensorPin, INPUT);
  pinMode(motionSensorPin, INPUT);
  pinMode(chlorinePumpPin, OUTPUT);
}

void loop() {
  sensors.requestTemperatures(); 
  float waterTemp = sensors.getTempCByIndex(0); // Read temperature

  int waterLevel = analogRead(waterLevelSensorPin);
  int pHValue = analogRead(pHsensorPin);
  int voltageValue = analogRead(voltageSensorPin);
  int currentValue = analogRead(currentSensorPin);
  int motionValue = digitalRead(motionSensorPin);

  EspSerial.print(waterLevel);
  EspSerial.print(",");
  EspSerial.print(pHValue);
  EspSerial.print(",");
  EspSerial.print(voltageValue);
  EspSerial.print(",");
  EspSerial.print(currentValue);
  EspSerial.print(",");
  EspSerial.print(motionValue);
  EspSerial.print(",");
  EspSerial.println(waterTemp);

  delay(1000);
}
