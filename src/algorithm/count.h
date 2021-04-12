#ifndef COUNT_H

#define ASSEMBLY_VELOCITY	20 		// 10cm/s; velocity of assembly line
#define FASTENER_L_MAX		50		// 24cm; maximum length of fastners
#define FASTENER_L_MIN		2.5		// 2.5cm; minimum length of fastners
#define DETECTION_CYCLE				// 50ms for each detection

#define THRESHOLD_HB		40
#define THRESHOLD_LB		10

#define WINDOW_SIZE			100
#define SLOW_CYCLE			FASTENER_L_MAX / ASSEMBLY_VELOCITY / WINDOW_SIZE * 1000

#define ITEM_THRESHOLD		10
// #define FAST_CYCLE		FASTENER_L_MIN / ASSEMBLY_VELOCITY / WINDOW_SIZE * 1000

// static float fast_window[WINDOW_SIZE];

#include <ArduinoQueue.h>

class Counter {
private:
	static ArduinoQueue<int> slow_window;
	static int count;
	static int previous_sum;
	static void changeCount(int sum);
public:
	static void readInput(float distance);
	static int readCount();
};

#endif