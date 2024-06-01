#include <SPI.h>
#include <RH_RF95.h>

#include <DHT.h>
#include <Adafruit_Sensor.h>

#include <TinyGPS++.h>
#include <SoftwareSerial.h>

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

TinyGPSPlus gps;
static const int RXPin = 4, TXPin = 3; 

SoftwareSerial ss(RXPin, TXPin);

double packetnum = 0;

void setup() 
{
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);
  ss.begin(9600);
   
  while (!Serial);
  Serial.begin(9600);
  delay(100);
 
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);
 
  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    while (1);
  }
     
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }
 
  // The default transmitter power is 13dBm, using PA_BOOST.
  rf95.setTxPower(14, false); // you can set transmitter powers from 5 to 23 dBm
  
  // Use a valid modem configuration
  rf95.setModemConfig(RH_RF95::Bw125Cr45Sf128);
}
 
void loop()
{
  String message = String(packetnum, 0) + "," +
                     String(gps.date.value(), 10)  + "," +
                     String(gps.time.value(), 10) + "," +
                     String(gps.location.lat(), 6)  + "," +
                     String(gps.location.lng(), 6)  + "," +
                     String(gps.altitude.meters(), 2) + "," +
                     String(dht.readHumidity(), 1) + "," +
                     String(dht.readTemperature(), 1) + "," +
                     String("0123456789ABCDEF0123456789ABCDEF0123");

  uint8_t dataoutgoing[message.length()];

  char databuf_m[message.length()];
  message.toCharArray(databuf_m, message.length()); 
  char databuf[strlen(databuf_m) + 1];
  sprintf(databuf, "%s", databuf_m);
  strcpy((char*)dataoutgoing, databuf);

  if(packetnum <= 50)
  { 
    Serial.println(databuf_m);
    rf95.send((uint8_t*)dataoutgoing, sizeof(dataoutgoing));
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

  if (rf95.waitAvailableTimeout(2000))
  { 
    // Should be a reply message for us now   
    if (rf95.recv(buf, &len))
    {
      // Process the received message
    }
    else
    {
      // Receive failed
    }
  }

  smartDelay(250);
}

static void smartDelay(unsigned long ms)
{
  unsigned long start = millis();
  do 
  {
    while (ss.available())
      gps.encode(ss.read());
  } 
  while (millis() - start < ms);
}
