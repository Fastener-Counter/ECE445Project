#include "screen.h"

static String Screen::message = "";
static bool Screen::test = false;
static SoftwareSerial Screen::screenSerial = SoftwareSerial(SCREEN_RX, SCREEN_TX);

int states;
int target_num;
unsigned char m_ReciverHeader;    //ATF Message Header char = @/#/$
unsigned short m_ReciverBodyID;   //ATF Message BodyID  0:GUI Swtich  100~65535:Body Msg
int m_ReciverVarInt;              //ATF Message int Val(Header=@)
float m_ReciverVarFloat;          //ATF Message float Val(Header=#)
String m_ReciverVarString;        //ATF Message String Val(Header=$)



void Screen::init(bool testFlag = false) {
    
    screenSerial.begin(9600);
    delay(50);
    screenSerial.print("@GUIS 0");
    screenSerial.print("@SET 109 ");
    screenSerial.println(0, 10);


    test = testFlag;
    message="";
}

int Screen::read() {


    if(ATFMessageService(2)){
        if(m_ReciverBodyID==118){
            if(m_ReciverVarInt==1){
                message="start";
            }
            if(m_ReciverVarInt==0){
                message="stop";
            }
        }

        if(m_ReciverBodyID==108){
            target_num=m_ReciverVarInt;
        }
        if(m_ReciverBodyID==116){
            message="clear";
        }

    }

    int status = 0;
    if (message=="start") status = 1;
    if (message=="stop") status = 2;
    if (message=="clear") status = 3;
    if (message[0]=="-") {
        status = 4;
    }
    message="";

    return status;

}

void Screen::send(String s) {
    screenSerial.println(s);
}

int Screen::available() {
    return screenSerial.available();
}


unsigned char ATFMessageService(unsigned char delaytimer)
{
  char n_TempChar;
  n_TempChar = Serial.available(); //获取可读取的字节数
  if(n_TempChar)
  {
    delay(delaytimer);
    n_TempChar = Serial.read(); //读取传入的串口数据的第一个字节
    while(n_TempChar!='@'&&n_TempChar!='#'&&n_TempChar!='$'&&n_TempChar>=0)
    {
      n_TempChar = Serial.read();
    }
    m_ReciverHeader = n_TempChar;
    m_ReciverBodyID = Serial.parseInt();//查找传入的串行数据流中的下一个有效的整数
    if(n_TempChar=='@')
    {
      m_ReciverVarInt = Serial.parseInt();
    }
    else if(n_TempChar=='#')
    {
      m_ReciverVarFloat = Serial.parseFloat();
    }
    else if(n_TempChar=='$')
    {
       Serial.read();
       m_ReciverVarString = Serial.readStringUntil('\r');  
    }
    else return 0;
    return 1;
  }
  return 0;
}