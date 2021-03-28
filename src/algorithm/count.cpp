#include "count.h"

static ArduinoQueue<int> Counter::slow_window(WINDOW_SIZE);
static int Counter::count = 0;
static int previous_sum = 0;

void Counter::changeCount(int sum) {
	if (sum < 10 && previous_sum >= 10) {
		count++
	}
	previous_sum = sum;
}

void Counter::readInput(float distance) {
	int detect_flag = (int)(distance>=THRESHOLD_LB && distance<=THRESHOLD_HB);
	if (slow_window.isFull()) slow_window.dequeue();
	slow_window.enqueue(detect_flag);
	changeCount(detect_flag.sum());
}

int readCount() {
	return count;
}