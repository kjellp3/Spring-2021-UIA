#include <Arduino.h>

unsigned long timer1 = 0;

void setup()
{
	Serial.begin(9600);
	pinMode(D0,INPUT_PULLUP);
	pinMode(D1,OUTPUT);
	pinMode(D2,OUTPUT);
	pinMode(D3,OUTPUT);
	
}

void loop()
{

	if (!digitalRead(D0)){
		analogWrite(D1,255);
		analogWrite(D2,255);
		analogWrite(D3,255);
	}

	else if (millis() - timer1 > 100){
		timer1 = millis();
		int potensiometer = analogRead(A1);
		

		int light1 = map(potensiometer,0,341,-5,260);
		light1 = constrain(light1,0,255);

		int light2 = map(potensiometer,341,682,-5,260);
		light2 = constrain(light2,0,255);

		int light3 = map(potensiometer,682,1023,-5,260);
		light3 = constrain(light3,0,255);

		analogWrite(D1,light1);
		analogWrite(D2,light2);
		analogWrite(D3,light3);
		Serial.println(potensiometer);
	}
}