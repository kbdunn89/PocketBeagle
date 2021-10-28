// gcc -shared -o leds.so -fPIC CTRLlines.c -lgpiod

#include <gpiod.h>
#include <unistd.h>
#include <stdio.h>

const char *chipname1 = "gpiochip1";
const char *chipname3 = "gpiochip3";

struct gpiod_chip *chip1;
struct gpiod_chip *chip3;

struct gpiod_line *CTRLEVEN;
struct gpiod_line *CTRLODD;

int init() {
    chip1 = gpiod_chip_open_by_name(chipname1);
    chip3 = gpiod_chip_open_by_name(chipname3);
    CTRLEVEN = gpiod_chip_get_line(chip3, 15);    // P1.33
    CTRLODD = gpiod_chip_get_line(chip1, 11);     // P1.30
    int err = 0;
    err |= gpiod_line_request_output(CTRLEVEN, "a", 0);
    err |= gpiod_line_request_output(CTRLODD, "a", 0);
    return err;
}

int turnOn() {
    int err = 0;
    err |= gpiod_line_set_value(CTRLEVEN, 1);
    err |= gpiod_line_set_value(CTRLODD, 1);
    return err;
}

int turnOff() {
    int err = 0;
    err |= gpiod_line_set_value(CTRLEVEN, 0);
    err |= gpiod_line_set_value(CTRLODD, 0);
    return err;
}

void release() {
    gpiod_line_release(CTRLEVEN);
    gpiod_line_release(CTRLODD);
    gpiod_chip_close(chip3);
    gpiod_chip_close(chip1);
}