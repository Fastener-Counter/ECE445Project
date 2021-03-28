#ifndef INFRARED_H

#include <Wire.h>
#include <Arduino.h>

#define INFRARED_ADDRESS       0x80 >> 1  // Arduino uses 7 bit addressing so we shift address right one bit
#define INFRARED_DISTANCE	   0x5E
#define INFRARED_SHIFT         0x35

class Infrared {
private:
    static int shift;
    Infrared();

public:
    static float read(int delay_time);
}


#endif