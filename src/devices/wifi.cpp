#include "wifi.h"

static int Wifi::read_flag = 0;
static String Wifi::message = "";
static bool Wifi::test = false;
static SoftwareSerial Wifi::wifiSerial = SoftwareSerial(WIFI_RX, WIFI_TX);

void Wifi::init(bool testFlag = false) {
    
    wifiSerial.begin(115200);
    // pinMode(0, INPUT_PULLUP);
    // pinMode(1, INPUT_PULLUP);
    test = testFlag;
    message="";
    delay(1000);
}

int Wifi::read() {

        if (wifiSerial.available()) {
            while (wifiSerial.available()) {
                char c = wifiSerial.read();
                message += c;
            }
        }

        if (message[message.length()-1]=='!') {
            if (test) {
                Serial.println(message);
            }

            int status = 0;
            if (message=="start!") status = 1;
            if (message=="stop!") status = 2;
            if (message=="clear!") status = 3;
            Serial.println("status"+String(status));
            message="";
            return status;
        }

        return 0;

}

void Wifi::send() {
    wifiSerial.println(Counter::getString());
    delay(20);
}

int Wifi::available() {
    return wifiSerial.available();
}