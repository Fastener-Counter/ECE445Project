#include "infrared.h"

static int Infrared::shift = 0;

Infrared::Infrared() {
    // Read the sift bit register from the module, used in calculating range
    Wire.beginTransmission(INFRARED_ADDRESS);    
    Wire.write(INFRARED_SHIFT);
    Wire.endTransmission();

    Wire.requestFrom(INFRARED_ADDRESS, 1);
    while(Wire.available() == 0);
    shift = Wire.read();
}


static float Infrared::read(int delay_time) {

    int distance = 0;
    byte high, low = 0;
    float test = 0;

    Wire.beginTransmission(INFRARED_ADDRESS);
    Wire.write(INFRARED_DISTANCE);
    Wire.endTransmission();

    Wire.requestFrom(INFRARED_ADDRESS, 2);

    while(Wire.available() < 2);

    high = Wire.read();
    low = Wire.read();
    // distance = (high * 16 + low)/16/(int)pow(2,shift); // Calculate the range in CM
    test = (high * 16 + low) / 16 / pow(2, shift);
    test = map(test, 2, 63.75, 4.0, 50.0);

    Serial.print("Distance is ");
    Serial.print(test);
    Serial.println("CM");

    delay(delay_time);
}
