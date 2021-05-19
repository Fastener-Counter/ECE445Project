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

String readMessage;
//unsigned time_now = millis();
int state;

***************************************************************/
#include "config.h"
int target;
int state=1;
int ret=1;
char usb_read='1';

void setup()
{
  // Start comms
//  Wire.begin();
  state = 1;
  target = 0;
  Serial.begin(9600);
  Serial.setTimeout(20);
  delay(50);  // Delay so everything can power up
  
  Wifi::init(true);
  Screen::init(true);  

  
// Read the sift bit register from the module, used in calculating range
//  Infrared inf_sensor;
//  Wifi::send("AT+GMR");
}


void loop()
{  
    Infrared::read(SLOW_CYCLE);
    char pin_read;
    if (Wifi::available() > 0){    
       usb_read=Wifi::read();
       if(usb_read=='1'){ ret=1;}
       if(usb_read=='2'){ ret=2;}
       if(usb_read=='3'){ ret=3;} 
    }
    if (Screen::available() > 0){    
       pin_read=Screen::read();
       if(pin_read=='1'){ ret=1;}
       if(pin_read=='2'){ ret=2;}
       if(pin_read=='3'){ ret=3;} 
    }
   
    if (ret > 0 && ret<3) {
      state = ret;
    }
    if (state==1) {
      Counter::readInput();
    }
    if (ret==3) {
      Counter::clearCount();
    }
  
}
