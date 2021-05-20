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
int last_time;

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
  last_time = millis();
  
//    Wifi::wifiSerial.listen();
//    Screen::screenSerial.listen();
// Read the sift bit register from the module, used in calculating range
//  Infrared inf_sensor;
//  Wifi::send("AT+GMR");
}


void loop()
{  
    ret = 0;
    Infrared::read(SLOW_CYCLE);
    char pin_read;
//    Serial.print(Wifi::available());
//    Serial.print(' ');
//    Serial.print(Screen::available());
//    Serial.println();

    if (Wifi::available() > 0){    
       ret = Wifi::read();
    }
    
    if (Screen::available() > 0){    
       ret=Screen::read();
       Serial.print("s");
       Serial.println(Screen::tar());
       
    }

    
    if (ret > 0 && ret<3) {
      state = ret;
    }
    if (state==1) {
      Counter::readInput();
    }
    
    if (Counter::readCount() >= Screen::tar()){
        state = 2;
    }
    Counter::dis_cur_num();
    if (ret==3) {
      Counter::clearCount();
    }

    Wifi::send();
  
}
