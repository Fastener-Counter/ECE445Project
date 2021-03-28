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

#include <Wire.h>

int distance = 0;                // Stores the calculated distance 
byte high, low = 0;              // High and low byte of distance
int shift = 0;                   // Value in shift bit register
float test=0;


#define ADDRESS       0x80 >> 1  // Arduino uses 7 bit addressing so we shift address right one bit
#define DISTANCE_REG  0x5E
#define SHIFT         0x35

void setup()
{
  // Start comms
  Wire.begin();
  Serial.begin(9600);
  
  delay(50);  // Delay so everything can power up
  
  // Read the sift bit register from the module, used in calculating range
  Wire.beginTransmission(ADDRESS);    
  Wire.write(SHIFT);
  Wire.endTransmission();
  
  Wire.requestFrom(ADDRESS, 1);
  while(Wire.available() == 0);
  shift = Wire.read();
}

void loop()
{
  // Request and read the 2 address bytes from the GP2Y0E02B
  Wire.beginTransmission(ADDRESS);
  Wire.write(DISTANCE_REG);
  Wire.endTransmission();
  
  Wire.requestFrom(ADDRESS, 2);
  
  while(Wire.available() < 2);
  
  high = Wire.read();
  low = Wire.read();
  
  distance = (high * 16 + low)/16/(int)pow(2,shift); // Calculate the range in CM
  test = (high * 16 + low)/16/pow(2,shift);
  test = map(test,2,63.75,4.0,50.0);
  
  Serial.print("Distance is ");
  Serial.print(test);
  Serial.println("CM");
  //Serial.println(test);
  
  
  delay(100);
}
