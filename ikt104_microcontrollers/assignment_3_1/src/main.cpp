#include <HTS221Sensor.h>
#include "DFRobot_RGBLCD.h"
#include <Wire.h>


#define I2C2_SCL PB10
#define I2C2_SDA PB11

TwoWire dev_i2c(I2C2_SDA, I2C2_SCL);
DFRobot_RGBLCD lcd(16, 2);
HTS221Sensor HumTemp(&dev_i2c);

bool lalala = true;
bool * tempOrhum = &lalala;


void change()
{
    lcd.clear();
    if (*tempOrhum)
            *tempOrhum = false;  
    else
        *tempOrhum = true;
}


void lcdtemp(float temperature){
    if (temperature < 20)
            lcd.setRGB(0,0,255);
        else if (temperature >= 20 && temperature <= 24)
            lcd.setRGB(255,165,0);
        else if (temperature > 25)
            lcd.setRGB(255,0,0);
        lcd.setCursor(0, 0);
        lcd.print("Temp: ");
        lcd.print(temperature);
        lcd.print(" C");
}

void lcdhum(float humidity)
{
    int light = map(humidity,0,100,0,255);
        lcd.setRGB(255-light,255-light,255);
        lcd.setCursor(0, 0);
        lcd.print("Humidity: ");
        lcd.print(humidity);
        lcd.print("%");
}

void setup()
{
    Serial.begin(9600);
    dev_i2c.begin();
    HumTemp.begin();
    HumTemp.Enable();
    lcd.init();
    pinMode(D2, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(D2), change, FALLING);
}

void loop()
{
    
    float humidity, temperature;
    HumTemp.GetHumidity(&humidity);
    HumTemp.GetTemperature(&temperature);


    if (*tempOrhum)
        lcdtemp(temperature);
    else
        lcdhum(humidity);


    Serial.print("Hum[%]: ");
    Serial.print(humidity, 2);
    Serial.print(" | Temp[C]: ");
    Serial.println(temperature, 2);
    
}