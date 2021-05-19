#ifndef SCREEN_H
#define SCREEN_H

#include <Arduino.h>
#include <SoftwareSerial.h>


#define TIME_MAX    200
#define SCREEN_RX     12
#define SCREEN_TX     13      // TX and RX port in Arduino

unsigned char ATFMessageService(unsigned char delaytimer);

class Screen {
    private:
        static String message;
    
    public:
        static SoftwareSerial screenSerial;
        static bool test;
        static int read();
        static void send(String s);
        static int available();
        static void init(bool testFlag);
};

#endif