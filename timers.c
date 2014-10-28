/*********************************************
 *********************************************
 *
 *  Project: Penn
 *  Script: timers.c
 *  Authors: Mike Lautman
 *********************************************
 *********************************************
 */

#include "timers.h"

#define base_clock_speed 16000000

bool set_clock_speed();



////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////
//
// SYSCLK Stuff
//
////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////

static int8_t clock_prescaler = 0;
////////////////////////////////////////////////
// SET_CLOCK_SPEED
//
// Functionality :
//   - set clock speed
//
// Parameters :
//
// Returns
//   - success or failure
bool set_clock_speed(void){
    // Set the system clock to clock speed
    clock_speed = base_clock_speed >> clock_prescaler;
    m_clockdivide(clock_prescaler);
    return CLKPR == clock_prescaler;
}




////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////
//
// LOOP Stuff
//
////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////

volatile static bool loop_running = false;
////////////////////////////////////////////////
// LOOP_ISSET
//
// Functionality :
//   - check to see if the loop is set and running
//
// Parameters
//   -
//
// Returns
//   - success or failure
bool loop_isSet(void){
    return loop_running;
}


////////////////////////////////////////////////
// SET_LOOP
//
// Functionality :
//   - setup main timer (timer_3) to run at loop_frequency = 1000Hz
//
// Parameters
//   -
//
// Returns
//   - success or failure
bool set_loop(void){
    // Set the system clock to 16MHz
    bool clock = set_clock_speed();

    // set clock prescaler to clock_speed/64
    int16_t timer_prescaler = 64;
    clear(TCCR3B, CS32);
    set(TCCR3B, CS31);
    set(TCCR3B, CS30);

    // put timer 3 into Mode 4 (Up to OCR3A)
    clear(TCCR3B, WGM33);
    set(TCCR3B, WGM32);
    clear(TCCR3A, WGM31);
    clear(TCCR3A, WGM30);

    // set OCR3A to be equal to 250 since we will always want a frequency of 1000KHz
    OCR3A = (int8_t)((base_clock_speed >> clock_prescaler)/(uint_32)timer_prescaler/1000);
    loop_running = true;
    return true;
}



////////////////////////////////////////////////
// LOOP_READY
//
// Functionality:
//   - Checks the loop timer (timer_3) to see if
//      1/1000 seconds have passed since last flag
//
// Parameters
//
// Returns
//   - ready or not as boolean
int8_t timer_3_overflow_register = TIFR3;
int8_t timer_3_overflow_flag = TOV3;
bool loop_ready(void){
    bool flag = check(timer_3_overflow_register, timer_3_overflow_flag);
    if (flag){
        set(timer_3_overflow_register, timer_3_overflow_flag);
    }
    return flag;
}


////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////
//
// STOPWATCH Stuff
//
////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////

static volatile uint32_t stopWatch_ovl_cnt = 0;
static volatile bool stopWatch_set = false;


////////////////////////////////////////////////
// STOPWATCH_ISSET
//
// Functionality :
//   - check to see if the loop is set and running
//
// Parameters
//   -
//
// Returns
//   - success or failure
bool stopwatch_isSet(void){
    return stopWatch_set;
}


////////////////////////////////////////////////
// CONFIG_STOPWATCH
//
// Functionality:
//   - setup timer (timer_1) to time things
//
// Parameters
//   - NONE!!
//
// Returns
//   - success or failure
//
bool config_stopWatch(void){
    cli();
    // Set the system clock to 16MHz
    bool clock = set_clock_speed();

    // set clock prescaler to clock_speed/8
    int16_t stopWatch_prescaler = 8;
    clear(TCCR1B, CS12);
    set(TCCR1B, CS11);
    clear(TCCR1B, CS10);

    // put timer 3 into Mode 0 (Up to 0xFFFF)
    clear(TCCR1B, WGM13);
    clear(TCCR1B, WGM12);
    clear(TCCR1A, WGM11);
    clear(TCCR1A, WGM10);


    stopWatch_set = true;
    clear_stopWatch();
    sei();
    return stopWatch_set;
}


////////////////////////////////////////////////
// CLEAR_STOPWATCH
//
// Functionality:
//   - clear timer (timer_1) counter to 0
//
// Parameters:
//
// Returns
//   - success or failure
bool clear_stopWatch(){
    // disable interupts since method is atomic
    cli();
    // clear ovl counter
    stopWatch_ovl_cnt = 0
    // clear Timer1 cnt (high byte first)
    TCNT1H = 0;
    TCNT1L = 0;

    // check Timer1 cnt ==0
    int16_t clk = (int16_t)TCNT1L;
    clk |= (int16_t)TCNT1H<<8;

    // re-enable interrupts
    sei();

    // return true if clock was reset
    return clk==0;
}


////////////////////////////////////////////////
// STOPWATCH_NOW ()
//
// Functionality:
//   - get the time since last stopWatch clear
//
// Parameters:
//
// Returns
//   - uint32_t (in 1/2,000,000 of second (could be bigger))
uint32_t stopWatch_now(void){
    // get current clock time
    int16_t clk = (int16_t)TCNT1L;
    clk |= (int16_t)TCNT1H<<8;

    // add all of the overflows
    uint32_t now = (stopWatch_ovl_cnt << 16) | (uint32_t)clk;
    return now;
}


////////////////////////////////////////////////
// STOPWATCH_GETDELTA
//
// Functionality:
//   - get difference between start and stopWatch_now
//
// Parameters:
//   - uint32_t start  : deltaStart
//
// Returns
//   - time delta : stopWatch_now - deltaStart
//   - uint32_t (in 1/2,000,000 of second (could be bigger))
uint32_t stopWatch_getDelta(uint32_t deltaStart){
    // subtract the start from now
    return stopWatch_now() - deltaStart;
}


////////////////////////
// Stopwatch timer ovfl
//   ~30times/second
////////////////////////
ISR(TIMER1_OVF){
    if (stopWatch_ovl_cnt + 1 =0){
        // ERR STATE!!!
    }
    stopWatch_ovl_cnt +=1;
}

