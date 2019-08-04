#include <Wire.h>
#include <Adafruit_MCP4725.h>

Adafruit_MCP4725 dac; // constructor

uint32_t dac_value;

void setup(void) {
  Serial.begin(9600);
  Wire.begin();
  dac.begin(0x60); // The I2C Address of the DAC 
  
}

void loop(void) {     
    if (Serial.available()>0) { //checks if there is a serial input
      dac_value=Serial.parseInt(); //reads serial input as a decimal value
      dac.setVoltage(dac_value, false); //sets DAC to dac_value
       }

     while (Serial.available()) { //needed to remove lingering inputs since pressing the enter button will cause Arduino to read an input of 0 and add it to the end of the previous value
          Serial.read();
          } 
}
