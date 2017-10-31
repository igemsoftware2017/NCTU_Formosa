#include <Bridge.h>
#include <BridgeClient.h>
#include <BridgeServer.h>
#include <BridgeSSLClient.h>
#include <BridgeUdp.h>
#include <Console.h>
#include <FileIO.h>
#include <HttpClient.h>
#include <Mailbox.h>
#include <Process.h>
#include <YunClient.h>
#include <YunServer.h>
#include <excel.h>
#include <SimpleDHT.h>
#include <Wire.h>
#include <Adafruit_BMP085_U.h>
#include <Adafruit_Sensor.h>
#include <SoftwareSerial.h>
#define dht_dpin 12
#include <math.h>
#include <SPI.h>

YunClient client;
Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);
int pinDHT=2;
SimpleDHT22 dht22;

boolean DEBUG = true;
int count = 0;
float temperature = 0;
float humidity =0;
char humdVal[100] = {'\0'};
char tempVal[100] = {'\0'};
char preVal[100] = {'\0'};
char distanceVal[100]={'\0'};
float pressure = 0;
int op=1;
int model=1;
char Switch[5];
int Switch_int = 999;
char Switch_sp1[5];
int Switch_sp1_int = 999;
char Switch_sp2[5];
int Switch_sp2_int = 999;
char Switch_sp3[5];
int Switch_sp3_int = 999;
int a=1;
int b=1;
int c=1;
int d1=0;
int d2=0;
int sp3v=1;
float e=0;
float f=0;
const byte trig =10;
const int echo = 9;
unsigned long d;
unsigned long ping(){
  digitalWrite(trig ,HIGH);
  delayMicroseconds(5);
  digitalWrite(trig, LOW);
  return pulseIn(echo, HIGH);
}
void displaySensorDetails(void)
{
  sensor_t sensor;
  bmp.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" hPa");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" hPa");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" hPa");  
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
} 

void setup() {
  Bridge.begin();
  Console.begin();
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode (trig, OUTPUT);
  pinMode (echo, INPUT);
  if(!bmp.begin())
  {
    Serial.print("Ooops, no BMP085 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
    displaySensorDetails();
    Wire.begin();
}
void loop() {
  delay(6000);
  Serial.print("humdity");
  Serial.print((float)humdity);
  Serial.println(" %");
  Serial.print("temperature");
  Serial.print((float)temperature);
  Serial.println(" C");
  d = (36.5-(ping()/58))*16.7;
  Serial.print("rainfall");
  Serial.print(d);
  Serial.println(" ml");
  sensors_event_t event;
  bmp.getEvent(&event);
  if (event.pressure)
  {
    Serial.print("Pressure:");
    Serial.print(event.pressure);
    Serial.println(" hPa ") ;
  }
   dtostrf(humd, 6, 6, humdVal);
   dtostrf(temp, 6, 6, tempVal);
   dtostrf(event.pressure, 6, 6, preVal);
   dtostrf(d, 6, 6, distanceVal);
   Bridge.put("Precp", humdVal);
   Bridge.put("Temperature", tempVal);
   Bridge.put("RH", preVal);
   Bridge.put("StnPres",distanceVal );
   if((op.excelop()>0.5)&&(model.excelmodel()>0.5)){
   Bridge.get("WATER_SPRAY",  Switch_sp1, 5);
   Switch[4] = '\0';
   Switch_sp1_int = atoi(Switch_sp1);
   Bridge.get("WATER_PUMP",  Switch_sp2, 5);
   Switch[4] = '\0';
   Switch_sp2_int = atoi(Switch_sp2);
   digitalWrite(4, Switch_sp2_int); 
   digitalWrite(4, Switch_sp1_int);
   } 
}

