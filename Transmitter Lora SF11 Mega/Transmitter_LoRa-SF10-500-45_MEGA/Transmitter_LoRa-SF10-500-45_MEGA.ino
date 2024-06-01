#include <SPI.h>
#include <RH_RF95.h>

#include <DHT.h>
#include <Adafruit_Sensor.h>

//#include <Wire.h>
//#include <Adafruit_INA219.h>

#include <TinyGPS++.h>
//#include <SoftwareSerial.h>

//#include <SD.h>

//#include <time.h>
 
#define RFM95_CS 10
#define RFM95_RST 9
#define RFM95_INT 2
 
// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 915.0
 
// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

// Temperature DHT22 Sensor
#define DHTPIN 5
#define DHTTYPE DHT22
DHT dht (DHTPIN, DHTTYPE);

//Adafruit_INA219 ss_current;

TinyGPSPlus gps;
//static const int RXPin = 10, TXPin = 11; 

// gpsPlus gps;
//SoftwareSerial ss(RXPin, TXPin);

double packetnum = 0;
float current = 0;


void setup() 
{
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);
  Serial.begin(9600);
  Serial1.begin(9600);
   
  while (!Serial);
  Serial.begin(9600);
  //delay(100);

  //ss_current.begin(9600);
 
  digitalWrite(RFM95_RST, LOW);
  //delay(10);
  digitalWrite(RFM95_RST, HIGH);
  //delay(10);
 
  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    while (1);
  }
     
  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM, Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }
 
  // The default transmitter power is 13dBm, using PA_BOOST.
  rf95.setTxPower(14, false); // you can set transmitter powers from 5 to 23 dBm
  rf95.setModemConfig(RH_RF95::Bw125Cr45Sf128);
}
 
void loop()
{
  //current = ss_current.getCurrent_mA();

  String message = String(packetnum, 0) + "," +
                     String(gps.date.value(), 10)  + "," +
                     String(gps.time.value(), 10) + "," +
                     String(gps.location.lat(), 6)  + "," +
                     String(gps.location.lng(), 6)  + "," +
                     String(gps.altitude.meters(), 1) + "," +
                     String(dht.readHumidity(), 1) + "," +
                     String(dht.readTemperature(), 1) + "," +
                     //String(current, 2) + "," +
                     String("0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF01234");
                     
                     
  //String message_end = "Fim da trasmissão";

  uint8_t dataoutgoing[message.length()];
  //uint8_t dataoutgoing_end[message_end.length()];

  char databuf_m[message.length()];
  message.toCharArray(databuf_m, message.length()); 
  char databuf[strlen(databuf_m) + 1];
  sprintf(databuf, "%s", databuf_m);
  strcpy((char*)dataoutgoing, databuf);

  if(packetnum <= 50)
  { 
    Serial.println(databuf_m);
    //Serial.print("Current: "); Serial.print(current); Serial.println(" mA");
    rf95.send((uint8_t*)dataoutgoing, sizeof(dataoutgoing));
      //delay(1000);
    packetnum++;
  }
  else 
  { 
    Serial.end();
  }

  rf95.waitPacketSent();
  // Now wait for a reply
  uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
  uint8_t len = sizeof(buf);
 
  //delay(20);
  if (rf95.waitAvailableTimeout(2000))
  { 
    // Should be a reply message for us now   
   if (rf95.recv(buf, &len))
   {
      //Serial.print("Got reply: ");
      //Serial.println((char*)buf);
      //Serial.print("RSSI: ");
      //Serial.println(rf95.lastRssi(), DEC);    
    }
    else
    {
      Serial.println("Receive failed");
    }
  }
  else
  {
    Serial.println("No reply, is there a listener around?");
  }
  

  //delay(1000);
  smartDelay(250);
  //Serial.println("Rodada " + i);
 
  
}
static void smartDelay(unsigned long ms)
{
  unsigned long start = millis();
  do 
  {
    while (Serial1.available())
      gps.encode(Serial1.read());
  } 
  while (millis() - start < ms);
  //Serial.println(millis());
}




