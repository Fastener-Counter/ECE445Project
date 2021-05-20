#include "count.h"

static ArduinoQueue<int> Counter::slow_window1(WINDOW_SIZE);
static ArduinoQueue<int> Counter::slow_window2(WINDOW_SIZE);
static ArduinoQueue<int> Counter::slow_window3(WINDOW_SIZE);


static int Counter::count = 0;
static int Counter::previous_sum = 0;
static int Counter::max_sum = 0;
static int Counter::detect_flag1 = 0;
static int Counter::detect_flag2 = 0;
static int Counter::detect_flag3 = 0;



static int Counter::changeCount(int sum1, int sum2, int sum3) {

	int sum = 0;
	if (sum1 > sum) sum = sum1;
	if (sum2 > sum) sum = sum2;
	if (sum3 > sum) sum = sum3;


	int sumwave=5*sum;
			
	//Screen::screenSerial.println("@GUIS 0");
	Screen::screenSerial.print("@SET 119 ");
	Screen::screenSerial.println(sumwave);



	Screen::screenSerial.print("@SET 109 ");
	Screen::screenSerial.println(count, 10);
	
	if (sum < ITEM_THRESHOLD && previous_sum >= ITEM_THRESHOLD) {
		count++; 
	}
		
	previous_sum = sum;

	return sum;
}

static void Counter::dis_cur_num(){
	Screen::screenSerial.print("@SET 109 ");
	Screen::screenSerial.println(count, 10);
}

static void Counter::readInput() {
	detect_flag1 = (int)(Infrared::distance1>=THRESHOLD_LB && Infrared::distance1<=THRESHOLD_HB);
	detect_flag2 = (int)(Infrared::distance2>=THRESHOLD_LB && Infrared::distance2<=THRESHOLD_HB);
	detect_flag3 = (int)(Infrared::distance3>=THRESHOLD_LB && Infrared::distance3<=THRESHOLD_HB);

	// Serial.print(Infrared::distance1);
	// Serial.print(' ');
	// Serial.print(Infrared::distance2);
	// Serial.print(' ');
	// Serial.println(Infrared::distance3);

	// Serial.print(detect_flag1);
	// Serial.print(' ');
	// Serial.print(detect_flag2);
	// Serial.print(' ');
	// Serial.println(detect_flag3);
	
	if (slow_window1.isFull()) slow_window1.dequeue();
	slow_window1.enqueue(detect_flag1);
	if (slow_window2.isFull()) slow_window2.dequeue();
	slow_window2.enqueue(detect_flag2);
	if (slow_window3.isFull()) slow_window3.dequeue();
	slow_window3.enqueue(detect_flag3);

	max_sum = changeCount(slow_window1.sum(), slow_window2.sum(), slow_window3.sum());
	// Serial.print(slow_window.sum());
	// Serial.print(' ');
	// Serial.println(count);
	
}

static int Counter::readCount() {
	return count;
}

static void Counter::clearCount() {
	count = 0;
}

static String Counter::getString() {
	String S = String(Infrared::distance1) + ',' +String(Infrared::distance2) + ',' + String(Infrared::distance3) + ',' + String(count) + ','
		+ String(detect_flag1) + ',' + String(detect_flag2) + ',' + String(detect_flag3) + ','
		+ String(slow_window1.sum()) + ',' + String(slow_window2.sum()) + ',' + String(slow_window3.sum()) + ',' + String(max_sum) + ','
		+ String(ITEM_THRESHOLD);
	return S; 
}


