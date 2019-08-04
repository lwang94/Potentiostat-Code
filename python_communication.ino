#include <Wire.h>
#include <Adafruit_MCP4725.h>
#define voltsIn A0

Adafruit_MCP4725 dac; // constructor

uint8_t python_input[2]={};
uint32_t dac_value=0;

void setup(void) {
  Serial.begin(9600);
  Wire.begin();
  dac.begin(0x60); // The I2C Address
}

void loop(void) {
    uint8_t adcValueRead[3] = {}; //MCP3426 will return three bytes that are two data bytes followed by a configuration byte (check MCP3426 datasheet (Table 5-4) for more details)  
    int16_t result=0; //final decimal value from the ADC after its been compiled from the two data bytes    
    
    if (Serial.available()>=2) {//checks if there are equal to or greater than 2 bytes in the serial input
      for (uint8_t i=0; i<2; ++i){
        python_input[i]=Serial.read(); //reads two bytes in the serial input coming from Python
      }
      dac_value=(( ( (int16_t)(python_input[0]) ) <<8) + python_input[1]); //concatenates the two bytes from Python
      dac.setVoltage(dac_value, false); //sets DAC to dac-value

      Wire.beginTransmission(0x6A); //I2C Address of the ADC
      Wire.write(0x88); //Hexadecimal command for the MCP3426, uses CH1 (check MCP3426 datasheet (section 5.2) for more details)
      Wire.endTransmission();
  
      delay(50); //wait small delay before requesting data from ADC
      
      Wire.requestFrom(0x6A, 3); //request three bytes from ADC 
      for (uint8_t i=0; i<2; ++i) {
        adcValueRead[i]=Wire.read(); //compiles the two data bytes
      }
      
      Serial.write(adcValueRead, 2); //write ADC reading to serial monitor
      
      while (Serial.available()) { //needed to remove lingering inputs
          Serial.read();
          }   
   }
}
