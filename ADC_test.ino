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
    uint8_t adcValueRead[3] = {}; //MCP3426 will return three bytes that are two data bytes followed by a configuration byte (check MCP3426 datasheet (Table 5-4) for more details)
     
    if (Serial.available()>0) { //checks if there is a serial input
      dac_value=Serial.parseInt(); //reads serial input as a decimal value
      dac.setVoltage(dac_value, false); //sets DAC to dac_value

      //Initialize ADC
      Wire.beginTransmission(0x6A); //I2C Address of the ADC
      Wire.write(0xA8); //Hexadecimal command for the MCP3426, uses CH2 (check MCP3426 datasheet (section 5.2) for more details)
      Wire.endTransmission();
  
      delay(50); //wait small delay before requesting data from ADC
      
      Wire.requestFrom(0x6A, 3); //request three bytes from ADC
      for (uint8_t i=0; i<2; ++i) {
        adcValueRead[i]=Wire.read(); //compiles the two data bytes
      }
      
      Serial.write(adcValueRead, 2); //write ADC reading to serial monitor

       while (Serial.available()) { //needed to remove lingering inputs since pressing the enter button will cause Arduino to read an input of 0 and add it to the end of the previous value
      Serial.read();
      } 
   }
}
