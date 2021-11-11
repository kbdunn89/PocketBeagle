// This file contain the functions to operate the Grove - Distance sensor.
// Use gpioinfo command for more infomation.
// We are using the SPI Grove connector. However, we are not using the SPI,
// we configure the pin P1.8 to GPIO in stead of CLK and we don't use P1.10 because it is not connected.

#include <gpiod.h>
#include <unistd.h>
#include <stdio.h>
#include <inttypes.h>
#include <sys/time.h>

//Global
const char *chipname0 = "gpiochip0";
struct gpiod_chip *chip0;
struct gpiod_line *pin1_8;
float duration = 0;

void init(){
    //Open GPIO chip
    chip0 = gpiod_chip_open_by_name(chipname0);
    
    //Open GPIO line
    pin1_8 = gpiod_chip_get_line(chip0, 13);   // P1.8
}

//Getting the duration of the signal
static int pulseIn(struct gpiod_line *pin){
    int count = 0;
    int timeout = 10000;
    struct timeval begin, current, pulseBegin, pulseEnd;
    gettimeofday(&begin, NULL);
    
    //Wait for the pulse to start
    count = 0;
    while (!gpiod_line_get_value(pin)){
        count++;
        //Only check for timeout every 1000 ticks
        if (count % 1000 == 0){
            gettimeofday(&current, NULL);
            if(current.tv_usec - begin.tv_usec >= timeout)
                return 0;
        }
    }
    
    //Save the time pulse started
    gettimeofday(&pulseBegin, NULL);
    
    //Wait for the pulse to stop
    count = 0;
    while (gpiod_line_get_value(pin)){
        count++;
        //Only check for timeout every 1000 ticks
        if (count % 1000 == 0){
            gettimeofday(&current, NULL);
            if(current.tv_usec - begin.tv_usec >= timeout)
                return 0;
        }
    }
    
    //Save the time pulse stopped
    gettimeofday(&pulseEnd, NULL);
    gpiod_line_release(pin);
    return pulseEnd.tv_usec - pulseBegin.tv_usec;
}

float MeasureInCentimeters(){
    //Set the pin to output to send trigger signal
    gpiod_line_request_output(pin1_8, "P1.8", 0);
    //Set the signal to high for at least 10 usec to triger the sensor
    gpiod_line_set_value(pin1_8, 1);
    usleep(10);
    gpiod_line_set_value(pin1_8, 0);
    
    gpiod_line_release(pin1_8);
    //Change to input to read the data
    gpiod_line_request_input(pin1_8, "P1.8");
    
    duration = pulseIn(pin1_8);
    //printf("Distance is: %7.3f cm\n", duration/58);
    return duration/58; //duration/29/2
}

float MeasureInInches(){
    //printf("Distance is: %7.3f in\n", MeasureInCentimeters()/2.54);
    return MeasureInCentimeters()/2.54;
}

//Release all the pins
void release() {
    gpiod_line_release(pin1_8);
    gpiod_chip_close(chip0);
}
