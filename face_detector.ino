#include <VarSpeedServo.h>
VarSpeedServo servo1;
String inputString = "";         // a string to hold incoming data
unsigned int cont=0;

void setup() 
{
  servo1.attach(9);

  Serial.begin(115200);
  Serial.println("Ready");
}


void loop() 
{

  signed int vel;
  unsigned int pos;
  
  if (Serial.available()) 
  {
    inputString = Serial.readStringUntil('!');
    vel = inputString.toInt();   

    if(inputString.endsWith("x"))
    {
      if (vel > 2)
        servo1.write(180, vel, false);    
      else if (vel < -2)
        servo1.write(0, -vel, false);    
      else
      {
        pos = servo1.read();
        servo1.write(pos, 255, false);       
      } 
    }
    else if(inputString.endsWith("o"))
    {
      cont++;
      if (cont >= 100)
      {
        pos = servo1.read();
        servo1.write(90, 20, true);        
        cont = 0;
 
      }
      else
      {
        pos = servo1.read();
        servo1.write(pos, 255, false);        
      }
      
            
    }
    inputString = "";

  }
}