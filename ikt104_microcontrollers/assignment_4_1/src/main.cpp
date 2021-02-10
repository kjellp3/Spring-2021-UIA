#include "DFRobot_RGBLCD.h"
#include <Wire.h>
#include <stm32l4xx_hal_iwdg.h>

IWDG_HandleTypeDef watchdog;

DFRobot_RGBLCD lcd(16, 2);

float counter = 0;
float partcount = 0;
volatile bool run = false;


void reset()
{
    HAL_IWDG_Refresh(&watchdog);
}

void keepcool()
{
    run = !run;
}

void setup()
{
    watchdog.Instance = IWDG;
    watchdog.Init.Prescaler = IWDG_PRESCALER_256;
    watchdog.Init.Reload = 1250; 
    watchdog.Init.Window = 0xFFF;
    HAL_IWDG_Init(&watchdog);
    lcd.init();
    pinMode(D2, INPUT_PULLUP);
    pinMode(D3, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(D2), reset, FALLING);
    attachInterrupt(digitalPinToInterrupt(D3), keepcool, FALLING);
}

void loop()
{
    lcd.setCursor(0, 0);
    float maincount = millis() - counter;
    lcd.print((maincount + partcount) / 1000.00);

    if (run)
    {
        partcount += maincount;
        
        while (run)
            HAL_IWDG_Refresh(&watchdog);
        
        counter = millis();
    }
}
