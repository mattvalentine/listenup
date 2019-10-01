#include <Adafruit_NeoPixel.h>

#define LEDPIN RGB_LED // connect the Data from the strip to this pin on the Arduino
#define NUMBER_PIEXELS 1 // the number of pixels in your LED strip
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMBER_PIEXELS, LEDPIN, NEO_GRB + NEO_KHZ800);

int switchpin = 2;
int switchlast = 0;

String lastLine = "                ";
String newLine = "                ";

void lcdsetup(){
  // serial for LCD
  Serial1.begin(9600);
  delay(50);
  Serial1.write(0x0012); //set baud to 9600 (on boot)
  delay(500);
    // go to upper left
  Serial1.write(0xFE);
  Serial1.write(0x80);
  Serial1.write(0xFE);
  Serial1.write(0x0C);
  Serial1.write("9600");
  delay(500);
  Serial1.write(0x7C);
  Serial1.write(0x9D);
  delay(500);
  Serial1.write(0xFE);
  Serial1.write(0x80);
  Serial1.write("0123456789ABCDEF");
  Serial1.write("ABCDEFGHIJKLMNOP");
  delay(2000);
  clearscreen();
}

void clearscreen(){  
  // go to upper left
  Serial1.write(0xFE);
  Serial1.write(0x80);

  // clear out the text
  Serial1.write("                ");
  Serial1.write("                ");
}

void setled(String textandcolor){
  if(textandcolor.length()>16){
    switch(textandcolor[16]) {
      case 'R':
        strip.setPixelColor(0, strip.Color(255,0,0));
        strip.show();
        break;
      case 'G':
        strip.setPixelColor(0, strip.Color(0,255,0));
        strip.show();
        break;
      case 'B':
        strip.setPixelColor(0, strip.Color(0,0,255));
        strip.show();
        break;
      case 'W':
        strip.setPixelColor(0, strip.Color(255,255,255));
        strip.show();
        break;
      case 'X':
        strip.setPixelColor(0, strip.Color(0,0,0));
        strip.show();
        break;
    }
  }
}

String formatLCD(String inString){
  if(inString.length()>16){
    return inString.substring(0,16);
  } else {
    while(inString.length()<16){
      inString = inString + " ";
    }
    return(inString);
  }
}

void setup() {  
  // prep the LED
  strip.begin();
  // setup the button
  pinMode(switchpin, INPUT_PULLUP);

  // spit out status to serial for monitoring
  // and listen for text from serial commands
  SerialUSB.begin(9600);
  SerialUSB.setTimeout(50);

  // setup lcd serial
  lcdsetup();
}

void loop() {
  // Read string from serial with text and LED
  // Format: "TEXTTEXTTEXTTEXT" + 'L'
  // 'L' is a char to indicate LED color R = Red X=off, etc
  String textandcolor = SerialUSB.readString();
  int switchStatus = digitalRead(switchpin);

  if(switchStatus != switchlast){
    if(switchStatus == 1){
      SerialUSB.println("NOW!");
    }
    switchlast = switchStatus;
  }

  // check for 17th char to indicate LED color
  setled(textandcolor);

  // convert the string to exactly 16 chars
  String newLine = formatLCD(textandcolor);
  
  // go to upper left
  Serial1.write(0xFE);
  Serial1.write(0x80);

  // scroll the text up a line and show new text
  Serial1.print(lastLine);
  Serial1.print(newLine);

  // save the current line so we can scroll it up.
  lastLine = newLine;
  
  // wait half a second so someone can read it
  delay(750);
}
