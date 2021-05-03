#ifndef WIFI_H
#define WIFI_H

#include <Arduino.h>
#include <SoftwareSerial.h>

#define WIFI_RX     12
#define WIFI_TX     13      // TX and RX port in Arduino
#define TIME_MAX    200

class Wifi {
    private:
        static String message;

    
    public:
        static SoftwareSerial wifiSerial;
        static bool test;
        static int read();
        static void send(String s);
        static int available();
        static void init(bool testFlag);
};

#endif