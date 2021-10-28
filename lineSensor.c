// gcc -shared -o sensor.so -fPIC lineSensor.c -lgpiod

#include <gpiod.h>
#include <unistd.h>
#include <stdio.h>

const char *chipname1 = "gpiochip1";
const char *chipname0 = "gpiochip0";

struct gpiod_chip *chip1;
struct gpiod_chip *chip0;

struct gpiod_line *QTR3;
struct gpiod_line *QTR4;
unsigned int val = 0x00;

void init() {
    // Open GPIO chip
    chip0 = gpiod_chip_open_by_name(chipname0);
    chip1 = gpiod_chip_open_by_name(chipname1);
    
    // Open GPIO lines
    QTR3 = gpiod_chip_get_line(chip0, 20);        // P1.20
    QTR4 = gpiod_chip_get_line(chip1, 10);        // P1.32
    gpiod_line_request_output(QTR3, "a", 0);
    gpiod_line_request_output(QTR4, "a", 0);
}

unsigned int readSensor(int delay) {
    gpiod_line_set_value(QTR3, 1);
    gpiod_line_set_value(QTR4, 1);
    
    // Charge the capacitors
    usleep(10);
    
    gpiod_line_release(QTR3);
    gpiod_line_release(QTR4);
    
    // Open switch line for input
    gpiod_line_request_input(QTR3, "a");
    gpiod_line_request_input(QTR4, "a");
    
    // Sleep for 1 msec
    usleep(delay);
    
    // Read input
    val = gpiod_line_get_value(QTR3);
    val |= gpiod_line_get_value(QTR4)<<1;
    
    gpiod_line_release(QTR3);
    gpiod_line_release(QTR4);
    
    gpiod_line_request_output(QTR3, "a", 0);
    gpiod_line_request_output(QTR4, "a", 0);
    return val;
}

void release() {
    gpiod_line_release(QTR3);
    gpiod_line_release(QTR4);
    gpiod_chip_close(chip0);
    gpiod_chip_close(chip1);
}