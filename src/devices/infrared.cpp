#include "infrared.h"

static float Infrared::distance1 = 0;
static float Infrared::distance2 = 0;
static float Infrared::distance3 = 0;

Infrared::Infrared() {
    // Read the sift bit register from the module, used in calculating range
}


static void Infrared::read(int delay_time) {

    
    distance1 = ((float)analogRead(A0))/1023*5*(-30.0)+67;
    distance2 = ((float)analogRead(A1))/1023*5*(-30.0)+67;
    distance3 = ((float)analogRead(A2))/1023*5*(-30.0)+67;

    


    // Serial.print("Distance is ");
    // Serial.print(test);
    // Serial.println("CM");

    delay(delay_time);
}
