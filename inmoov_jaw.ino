#include <VarSpeedServo.h>

VarSpeedServo myservo;  // create servo object to control a servo
String inputString = "";
const int servoPin = 9; // the digital pin used for the servo


void setup() {
  Serial.begin(128000);
  myservo.attach(servoPin);  // attaches the servo on pin 9 to the servo object
  myservo.write(50, 255, true); // set the initial position of the servo, as fast as possible, wait until done
}

void loop() {
  signed int receivedValue;
  signed int newValue;

  if (Serial.available()) {
    inputString = Serial.readStringUntil('!');
    receivedValue = inputString.toInt();

    if (receivedValue == 1) {
      while (receivedValue == 1) {
        myservo.write(50, 230, true);  // move the servo to 180, slow speed, wait until done
        myservo.write(180, 255, true);
        if (Serial.available()) {
            inputString = Serial.readStringUntil('!');
            newValue = inputString.toInt();
          if (newValue == 0 || newValue == 1) {
            receivedValue = newValue;
          }
        }
      }
    } else if (receivedValue == 0) {
      myservo.write(50, 255, true);
    }
  }
}
