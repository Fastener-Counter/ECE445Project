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

String readMessage;
//unsigned time_now = millis();
int state;

void setup()
{
  // Start comms
//  Wire.begin();
  state = 1;
  Serial.begin(9600);
  
  delay(50);  // Delay so everything can power up
  Wifi::init(true);
  // Read the sift bit register from the module, used in calculating range
//  Infrared inf_sensor;
//  Wifi::send("AT+GMR");
}

void loop()
{
  // Request and read the 2 address bytes from the GP2Y0E02B
  Infrared::read(SLOW_CYCLE);
  //float distance1 = ((float)analogRead(0))/1023*5*(-30.0)+67;
//  Serial.println(Counter::readCount());
//  time_now = millis();
   int ret = Wifi::read();
//   Serial.println(state);
   if (ret > 0 && ret!=3) {
      state = ret;
   }
   if (state==1) {
      Counter::readInput();
   }
   else if (ret==3) {
      Counter::clearCount();
   }

//  while (millis() < time_now + 100) {}

//  Serial.println(((float)analogRead(2))/1023*5*(-30.0)+67);
  
  
}
