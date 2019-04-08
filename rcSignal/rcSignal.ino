//-------------------------------------------------------------------
// rcSingal.ino
//
// Turn desired control inputs into ppm signal. This is sent via
// audio cable to the radio transmitter and then to the RC plane.
//
// ISR code from: https://quadmeup.com/generate-ppm-signal-with-arduino/


//--------------------------CHANNEL MAPPING--------------------------
// 0: Throttle 1000 ppm is off, 2000 is full thrust
// 1: Ailerons 1500 ppm is neutral, 1000 is full right roll, 2000 is full left roll
// 2: Elevator 1500 ppm is neutral, 1000 is full down, 2000 is full up
// 3: Rudder   1500 ppm is neutral, 1000 is yaw right, 2000 is yaw left
// 4:
// 5: Flaps    1000 ppm is 0 degree flap, 2000 is full flap

//--------------------------GLOBAL VARIABLES-------------------------
#define chanel_number 6  //set the number of channels
#define default_servo_value 1000  //set the default servo value
#define PPM_FrLen 22500  //set the PPM frame length in microseconds (1ms = 1000µs)
#define PPM_PulseLen 300  //set the pulse length
#define onState 1  //set polarity of the pulses: 1 is positive, 0 is negative
#define sigPin 7  //set PPM signal output pin on the arduino
#define begin_of_msg 123 //set signature of message start
//-------------------------------------------------------------------



/*this array holds the servo values for the ppm signal
 change theese values in your code (usually servo values move between 1000 and 2000)*/
int ppm[chanel_number];
int currChan;

void setup() {
  // Open serial port
  Serial.begin(9600);
//  Serial.setTimeout(50);
  
  //initiallize default ppm values
  for(int i=0; i<chanel_number; i++){
    ppm[i]= default_servo_value;
  }
  currChan = 0;

  pinMode(sigPin, OUTPUT);
  digitalWrite(sigPin, !onState);  //set the PPM signal pin to the default state (off)
  
  cli();
  TCCR1A = 0; // set entire TCCR1 register to 0
  TCCR1B = 0;
  
  OCR1A = 100;  // compare match register, change this
  TCCR1B |= (1 << WGM12);  // turn on CTC mode
  TCCR1B |= (1 << CS11);  // 8 prescaler: 0,5 microseconds at 16mhz
  TIMSK1 |= (1 << OCIE1A); // enable timer compare interrupt
  sei();
}

void loop() {
  receivePWMInput();
}

void receivePWMInput() {
  static int val = 100;
  if (Serial.available()) {
    int temp = Serial.read();
    if (currChan >= chanel_number && temp == begin_of_msg) {
      currChan = 0;
//      Serial.println();
    }
    else {
      ppm[currChan] = map(temp, 0, 255, 1000, 2000);
//      Serial.println("    Channel " + String(currChan) + ": " + String(ppm[currChan])); 
      currChan++;
    }
    


    
//    if (Serial.read() == begin_of_msg) {
//      // Read the commands from the python script
//      for (int i = 0; i < chanel_number; i++) {
//        int temp = Serial.read();
//        ppm[i] = map(temp, 0, 255, 1000, 2000);
//      }
//      // Print out the commands read
//      Serial.println();
//      for (int i = 0; i < chanel_number; i++) {
//       Serial.println("    Channel " + String(i) + ": " + String(ppm[i])); 
//      }
//    }
  }
}

// The Interrupt Service Routine which calculates the correct
// PPM signal based on the channel values
ISR(TIMER1_COMPA_vect){ 
  static boolean state = true;
  
  TCNT1 = 0;
  
  if(state) {  //start pulse
    digitalWrite(sigPin, onState);
    OCR1A = PPM_PulseLen * 2;
    state = false;
  }
  else{  //end pulse and calculate when to start the next pulse
    static byte cur_chan_numb;
    static unsigned int calc_rest;
  
    digitalWrite(sigPin, !onState);
    state = true;

    if(cur_chan_numb >= chanel_number){
      cur_chan_numb = 0;
      calc_rest = calc_rest + PPM_PulseLen;// 
      OCR1A = (PPM_FrLen - calc_rest) * 2;
      calc_rest = 0;
    }
    else{
      OCR1A = (ppm[cur_chan_numb] - PPM_PulseLen) * 2;
      calc_rest = calc_rest + ppm[cur_chan_numb];
      cur_chan_numb++;
    }     
  }
}
