/*************************************************** 
  This is an example for our Adafruit 16-channel PWM & Servo driver
  Servo test - this will drive 8 servos, one after the other on the
  first 8 pins of the PCA9685

  Pick one up today in the adafruit shop!
  ------> http://www.adafruit.com/products/815
  
  These drivers use I2C to communicate, 2 pins are required to  
  interface.

  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// you can also call it with a different address you want
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);
// you can also call it with a different address and I2C interface
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(&Wire, 0x40);

// Depending on your servo make, the pulse width min and max may vary, you 
// want these to be as small/large as possible without hitting the hard stop
// for max range. You'll have to tweak them as necessary to match the servos you
// have!
#define SERVOMIN  50 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  400 // this is the 'maximum' pulse length count (out of 4096)

// our servo # counter
uint8_t servonum = 0;
/*
5 250 down - 80 up arm
4 100 down - 260 up shoulder
3 270 down - 460 up arm
2 90 down - 260 up shoulder
1 100 right - 275 middle - 460 left look
0 90 up - 250 down nod
*/

void setup() {
  Serial.begin(9600);
  //Serial.println("8 channel Servo test!");

  pwm.begin();
  
  pwm.setPWMFreq(50);  // Analog servos run at ~60 Hz updates
pwm.setPWM(0, 0, 90);
pwm.setPWM(1, 0, 280);
pwm.setPWM(2, 0, 90);
pwm.setPWM(3, 0, 270);
pwm.setPWM(4, 0, 100);
pwm.setPWM(5, 0, 250); //250 down, 90 front
Serial.println("please send servo, angel to serial");
  delay(100);
}

// you can use this function if you'd like to set the pulse length in seconds
// e.g. setServoPulse(0, 0.001) is a ~1 millisecond pulse width. its not precise!
/*void setServoPulse(uint8_t n, double pulse) {
  double pulselength;
  
  pulselength = 1000000;   // 1,000,000 us per second
  pulselength /= 60;   // 60 Hz
  //Serial.print(pulselength); Serial.println(" us per period"); 
  pulselength /= 4096;  // 12 bits of resolution
  //Serial.print(pulselength); Serial.println(" us per bit"); 
  pulse *= 1000000;  // convert to us
  pulse /= pulselength;
  //Serial.println(pulse);
  pwm.setPWM(n, 0, pulse);
}
*/

/*
0 90 up - 250 down nod
1 100 right - 280 middle - 460 left look
2 90 down - 260 up shoulder
3 270 down - 460 up arm
4 100 down - 260 up shoulder
5 250 down - 80 up arm
*/
int bounds[] = {90, 250, 100, 460, 90, 260, 270, 460, 100, 260, 250, 80};

int percent2angel(int servo, int angel) {
  int lower = bounds[servo*2];
  int upper = bounds[servo*2+1];
  Serial.print(lower);
  Serial.print(",");
  Serial.print(upper);
  Serial.print(".");
  int finalAngel = lower + (upper-lower) * angel / 100;
  Serial.println(finalAngel);
  return finalAngel;
}

void servos(int a0, int a1, int a2, int a3, int a4, int a5, int delayTime) {
  pwm.setPWM(0, 0, percent2angel(0, a0));
  pwm.setPWM(1, 0, percent2angel(1, a1));
  pwm.setPWM(2, 0, percent2angel(2, a2));
  pwm.setPWM(3, 0, percent2angel(3, a3));
  pwm.setPWM(4, 0, percent2angel(4, a4));
  pwm.setPWM(5, 0, percent2angel(5, a5));
  delay(delayTime);
}

void dance() {
  servos(0,50,0,0,0,0,500);
  servos(0,0,50,50,0,50,500);
  servos(0,0,50,0,50,0,500);
  servos(30,0,60,0,90,0,500);
  servos(80,0,20,0,40,0,500);
  servos(0,50,0,0,0,0,500);
}

void loop() {
  // Drive each servo one at a time
  while(Serial.available() > 0) {
    int servo = Serial.parseInt();
    int angel = Serial.parseInt();
    if (servo == 99) {
      dance();
      return;
    }
    if (servo = 100) {
      servos(0,50,0,0,0,0,500);
      return;
    }
    Serial.print(servo);
    Serial.print(" = ");
    Serial.println(angel);
    pwm.setPWM(servo, 0, angel);
  }
  

  /*for (uint16_t pulselen = SERVOMAX; pulselen > SERVOMIN; pulselen--) {
    delay(2);
    pwm.setPWM(servonum, 0, pulselen);
  }*/
//460-90
/*  for(int i = 250; i >= 90; i-=30){
    Serial.println(i);
    pwm.setPWM(4, 0, i);
    pwm.setPWM(5, 0, i);
    delay(100);
  }
 */
delay(1000);
  //servonum ++;
  //if (servonum > 7) servonum = 0;
}

/* Code below are for led bars.
1. Init as 'ready for contest' from serial
2. Start with 'A' or 'B', instructed from serial
3. A starts to count down until button is pressed
4. When button is pressed for A, count down stops, triggers B count down
5. B counts down until button is pressed
6. When button B is pressed, switch side
7. If A or B is done, disable the other side's button
8. When both A and B are done, celebrate for all done
9. Can modify the time remaining on the fly

Also consider how to integrate this contest part into the robot part
Robot receives postures from Serial in normal situations, when in contest mode,
it will be taken over by the contest model, switching side will change the posture, that is all.

*/

int current_mode = 0;
#def CONTEST 1
#def POSTURE 0
float _time_remaining[] = {0.0, 0.0};
bool _btn_enabled[] = {true, true};
#def BtnA 3;
#def BtnB 4;

// called when receiving ready signal from serial, A side has timeA seconds, B side has timeB seconds
void getReady(int timeA, int timeB) {
  // todo: enter contest mode, pause receiving postures
  current_mode = CONTEST;
  // todo: robot both arms up, say "Ready"
  // todo: reset the light bars with an animation effect
  // set time remaining for both A and B, reset buttons
  _time_remaining[0] = timeA;
  _time_remaining[1] = timeB;
  _btn_enabled[0] = true;
  _btn_enabled[1] = true;
  pinMode(BtnA, INPUT);
  pinMode(BtnB, INPUT);
}

// called when receiving query from serial, if setA, setB equals to -1, just return the time remaing, otherwise set the time remaining
void timeRemaining(float setA, float setB) {
  if (setA > 0) {
    _time_remaining[0] = setA;
  }
  if (setB > 0) {
    _time_remaining[1] = setB;
  }
  Serial.print(_time_remaining[0]);
  Serial.print(" ");
  Serial.print(_time_remaining[1]);
  Serial.print(" ");
}

// called when receiving start signal from serial with parameter side A or B
void startContestWith(int side) {
  while(true) {
    if (_time_remaining[side] + _time_remaining[otherSide] == 0.001) {
      // all done
      allDone();
      return false;
    }
    countDown(side);
    //switch side
    int side = ((side == 0) ? 1:0);
  }
}

// function to count down, return true if button pressed or time up
void countDown(int side) {
  int& remaining = _time_remaining[side];
  int otherSide = ((side == 0) ? 1:0);
  while(true) {
    // if time up for this side, disable the other side's button and switch side
    if (remaining < 0.001) {
      disableButton(otherSide);
      _btn_enabled[otherSide] = false;
      // return true to count down the other side
      return;
    }
    // if button is pressed, switch side)
    if (digitalRead(side == 0 ? BtnA:BtnB)) {
      return;
    }
    remaining -= 0.01;
    sleep(10);
    // update led bar
    updateLEDbar();
  }
}

void updateLEDbar() {
  // todo: use time_remaining to update led status
}

void allDone() {
  // send serial "all done, hurra"
  Serial.println("Contest done, hurra");
  // todo: go back to normal mode to receive postures
  current_mode = POSTURE;
}

// NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// released under the GPLv3 license to match the rest of the AdaFruit NeoPixel library

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1
#define PIN            6

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS      16

// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest
// example for more information on possible values.
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

int delayval = 500; // delay for half a second

void setup() {
  // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
#if defined (__AVR_ATtiny85__)
  if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
#endif
  // End of trinket special code

  pixels.begin(); // This initializes the NeoPixel library.
}

void loop() {

  // For a set of NeoPixels the first NeoPixel is 0, second is 1, all the way up to the count of pixels minus one.

  for(int i=0;i<NUMPIXELS;i++){

    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(0,150,0)); // Moderately bright green color.

    pixels.show(); // This sends the updated pixel color to the hardware.

    delay(delayval); // Delay for a period of time (in milliseconds).

  }
}
