#include "wifi.h"

static String Wifi::message = "";
static bool Wifi::test = false;
static SoftwareSerial Wifi::wifiSerial = SoftwareSerial(WIFI_RX, WIFI_TX);

char c;
int time;

void Wifi::init(bool testFlag = false) {
    
    wifiSerial.begin(9600);
    delay(1000);
    wifiSerial.println("AT+CIPMUX=1");
    delay(1000);
    wifiSerial.println("AT+CIPSERVER=1");
    test = testFlag;
    message="";
}

int Wifi::read() {

        while (wifiSerial.available()) {
            c = wifiSerial.read();
            message += c;
        }

        if (message[message.length()-1]=='!') {
            message = message.substring(message.lastIndexOf(':')+1, message.length()-1);
            if (test) {
                Serial.println(message);
            }

            int status = 0;
            if (message=="start") status = 1;
            if (message=="stop") status = 2;
            if (message=="clear") status = 3;
            if (message[0]=="-") {
                status = 4;
                //ip = message.substring(1, message.length());
                
            }
            message="";

            return status;
        }

        return 0;

}

void Wifi::send(String s) {
    wifiSerial.println(s);
}

int Wifi::available() {
    return wifiSerial.available();
}