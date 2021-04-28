/***************************************************************
  Arduino GP2Y0E03 example code
  Gets range from GP2Y0E03 and prints it to the serial monitor.

Pin Connect:
GP2Y0E03            Arduino
1.PIN--VCC          3V3
2.PIN--Vout(A)      Not Connect
3.PIN--GND          GND
4.PIN--VIN(IO)      3V3
5.PIN--GPIO1        3V3
6.PIN--SCL          A5
7.PIN--SDA          A4

***************************************************************/
#include "config.h"

void setup()
{
  // Start comms
  //Wire.begin();
  Serial.begin(9600);
  
  delay(50);  // Delay so everything can power up
  
  // Read the sift bit register from the module, used in calculating range
//  Infrared inf_sensor;
}

void loop()
{
  // Request and read the 2 address bytes from the GP2Y0E02B
  Infrared::read(SLOW_CYCLE);
  //float distance1 = ((float)analogRead(0))/1023*5*(-30.0)+67;
  Counter::readInput();
//  Serial.println(Counter::readCount());
  
//  Serial.println(((float)analogRead(2))/1023*5*(-30.0)+67);
  
  
}
