#include <SPI.h>
#include <RH_RF95.h>
#include <DHT.h>
#include <Adafruit_Sensor.h>
#include <TinyGPS++.h>

#define RFM95_CS 10
#define RFM95_RST 9
#define RFM95_INT 2
#define RF95_FREQ 915.0

RH_RF95 rf95(RFM95_CS, RFM95_INT);
#define DHTPIN 5
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
TinyGPSPlus gps;

double packetnum = 0;

void setup() 
{
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);
  Serial.begin(9600);
  Serial1.begin(9600);

  while (!Serial);
  delay(100);

  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  if (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    while (1);
  }

  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }

  rf95.setTxPower(14, false);
  rf95.setModemConfig(RH_RF95::Bw125Cr45Sf128);
}

void loop()
{
  String message = String(packetnum, 0) + "," +
                     String(gps.date.value(), 10)  + "," +
                     String(gps.time.value(), 10) + "," +
                     String(gps.location.lat(), 6)  + "," +
                     String(gps.location.lng(), 6)  + "," +
                     String(gps.altitude.meters(), 1) + "," +
                     String(dht.readHumidity(), 1) + "," +
                     String(dht.readTemperature(), 1) + "," +
                     String("0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF01234");

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
  uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
  uint8_t len = sizeof(buf);

  if (rf95.waitAvailableTimeout(2000))
  { 
    if (rf95.recv(buf, &len))
    {
      Serial.println("Got reply: ");
      Serial.println((char*)buf);
      Serial.print("RSSI: ");
      Serial.println(rf95.lastRssi(), DEC);    
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

  smartDelay(250);
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
}
