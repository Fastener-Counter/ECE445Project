#ifndef COUNT_H
#define COUNT_H

#define ASSEMBLY_VELOCITY	20 		// 10cm/s; velocity of assembly line
#define FASTENER_L_MAX		20		// 24cm; maximum length of fastners
#define FASTENER_L_MIN		2.5		// 2.5cm; minimum length of fastners
#define DETECTION_CYCLE				// 50ms for each detection

#define THRESHOLD_HB		40
#define THRESHOLD_LB		10

#define WINDOW_SIZE			20
#define SLOW_CYCLE			FASTENER_L_MAX / ASSEMBLY_VELOCITY / WINDOW_SIZE * 1000

#define ITEM_THRESHOLD		6
// #define FAST_CYCLE		FASTENER_L_MIN / ASSEMBLY_VELOCITY / WINDOW_SIZE * 1000

// static float fast_window[WINDOW_SIZE];

#include <ArduinoQueue.h>
#include "../devices/infrared.h"
#include "../devices/screen.h"

class Counter {
private:
	static ArduinoQueue<int> slow_window1;
	static ArduinoQueue<int> slow_window2;
	static ArduinoQueue<int> slow_window3;
	static int count;
	static int previous_sum;
	static int max_sum;
	static int detect_flag1;
	static int detect_flag2;
	static int detect_flag3;
	static int changeCount(int sum1, int sum2, int sum3);
public:
	static void readInput();
	static int readCount();
	static void clearCount();
	static String getString();
	static void dis_cur_num();
};

#endif