// OneWire interface
#include <OneWire.h>
// Digital sensor library
#include <DallasTemperature.h>
// LCD library code:
#include <LiquidCrystal.h>

// One wire BUS pin
#define ONE_WIRE_BUS 50

OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensors(&oneWire);


// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 4, en = 5, d4 = 10, d5 = 11, d6 = 12, d7 = 13;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// Temperature
int SensorPin = 0;
int Temperature = 0;
double tempC;
int greenLED = 22;
int yellowLED = 24;
int redLED = 26;
float digTemp = 0.0;
int command = 0;

// Arduino's NAME
const int ID = 1000;

void handleLED(double temp) {
    if(temp <= 40) {
        digitalWrite(greenLED, HIGH);
        digitalWrite(yellowLED, LOW);
        digitalWrite(redLED, LOW);
    } else if (temp <= 60) {
        digitalWrite(greenLED, LOW);
        digitalWrite(yellowLED, HIGH);
        digitalWrite(redLED, LOW);
    } else {
        digitalWrite(greenLED, LOW);
        digitalWrite(yellowLED, LOW);
        digitalWrite(redLED, HIGH);
    }
}
void setup() {

    // Configures the reference voltage on analog pins.
    // Possible values:
    // DEFAULT: default voltage
    // INTERNAL: 1.1V on ATmega168, ATmega328P
    //           2.56V on ATmega8
    // INTERNAL1V1: built-in 1.1V reference (Arduino Mega only)
    // INTERNAL2V56: built in 2.56V (Arduino Mega only)
    // EXTERNAL: voltage applied to the AREF pin (0-5V) 
    analogReference(DEFAULT);

    Serial.begin( 9600 );

    // set up the LCD's number of columns and rows:
    lcd.begin(16, 2);
    // Print a message to the LCD.
    lcd.print("Temperature meter!");

    pinMode(greenLED, OUTPUT);
    pinMode(yellowLED, OUTPUT);
    pinMode(redLED, OUTPUT);

    delay(1000);
    lcd.clear();
}

void loop() {
    // Read temperature every loop
    Temperature = analogRead(SensorPin);
    tempC = (Temperature * 500) / 1023.0;

    sensors.requestTemperatures();

    digTemp = sensors.getTempCByIndex(0);

    handleLED(int(digTemp));

    // Write the result to the LCD
    // ANALOG
    lcd.clear();
    lcd.setCursor( 0, 0);
    lcd.print(tempC);
    lcd.print((char)223);
    lcd.print("C");
    // DIGITAL
    lcd.setCursor( 0, 1);
    lcd.print(digTemp);
    lcd.print((char)223);
    lcd.print("C");

    // Wait for ping before sending serial

    if (Serial.available() > 0) {
        if (Serial.peek() == 'c') {
            Serial.read();
            command = Serial.parseInt();
            /* 
               Do the harlem SHAKE
               */
            if (command == 7) {
                Serial.println(ID);
                Serial.println(ONE_WIRE_BUS);
                Serial.println(SensorPin);
                Serial.println(digTemp);
                command = 0;
            }
        }
        while (Serial.available() > 0)
            Serial.read();
    }

    // Wait
    delay(1000);
}

