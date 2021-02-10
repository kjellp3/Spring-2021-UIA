#include <Arduino.h>


void setup(){
    Serial.begin(9600);

}


void loop()
{

    if (Serial.available() > 0){      
        char byte = Serial.read();         
        if (byte == '0')
            analogWrite(A0,0);
        else if (byte == '1')
            analogWrite(A0,255);
    }
}