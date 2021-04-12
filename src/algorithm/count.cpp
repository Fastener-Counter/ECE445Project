#include "count.h"

static ArduinoQueue<int> Counter::slow_window(WINDOW_SIZE);
static int Counter::count = 0;
static int Counter::previous_sum = 0;

static void Counter::changeCount(int sum) {
	if (sum < ITEM_THRESHOLD && previous_sum >= ITEM_THRESHOLD) {
		count++; 
	}
	previous_sum = sum;
}

static void Counter::readInput(float distance) {
	int detect_flag = (int)(distance>=THRESHOLD_LB && distance<=THRESHOLD_HB);
	if (slow_window.isFull()) slow_window.dequeue();
	slow_window.enqueue(detect_flag);
	changeCount(slow_window.sum());
	Serial.print(slow_window.sum());
	Serial.print(' ');
	Serial.println(count);
}

static int Counter::readCount() {
	return count;
}