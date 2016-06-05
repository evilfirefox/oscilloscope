#include <SoftwareSerial.h>
#define BAUDRATE 9600
#define PIN_READ A0
#define BUFFER_SIZE 128
#define DEFAULT_PRECISION 50

int buffer[BUFFER_SIZE];
int currentPosition = 0;

void setup() {
  Serial.begin(BAUDRATE);
  pinMode(PIN_READ, INPUT);
}

void loop() {
  buffer[currentPosition] = analogRead(PIN_READ);
  currentPosition++;
  Serial.println(buffer[currentPosition]*0.0049);
  delay(DEFAULT_PRECISION);
  if (currentPosition == BUFFER_SIZE) {
      //Serial.write(buffer, BUFFER_SIZE);
      currentPosition = 0;
  }
}
