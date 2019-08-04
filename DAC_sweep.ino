#include <Wire.h>
#include <Adafruit_MCP4725.h>

Adafruit_MCP4725 dac; // constructor

//IMPORTANT: THESE ARE THE VARIABLES YOU CHANGE FOR EACH SWEEP EXPERIMENT
uint32_t dac_value=0; // initial dac value
uint32_t increment=100; //step size of sweep
uint32_t wait_time=500; //time between measurements so results can be written down

//Executes sweep
void setup(void) {
  Serial.begin(9600);
  Wire.begin();
  dac.begin(0x60); // The I2C Address of the DAC 
  
}

void loop(void) {     
     dac_value=Serial.parseInt(); //reads serial input as a decimal value
     dac.setVoltage(dac_value, false); //sets DAC to dac_value

     delay(wait_time); //stops the program temporarily

     dac_value+=increment //increases the dac value by the step size
}
