#include <SPI.h>
#include <RH_RF95.h>

#define RFM95_CS 10
#define RFM95_RST 9
#define RFM95_INT 2
#define RF95_FREQ 915.0

RH_RF95 rf95(RFM95_CS, RFM95_INT);

void setup() 
{
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);
  Serial.begin(9600);
   
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
  if (Serial.available()) {
    int len = Serial.available();
    uint8_t buf[len];
    Serial.readBytes(buf, len);
    rf95.send(buf, len);
    rf95.waitPacketSent();
    Serial.println("Transmited message via LoRa");
  }
  smartDelay(250);
}

static void smartDelay(unsigned long ms)
{
  unsigned long start = millis();
  while (millis() - start < ms) {
    // adicionar qualquer processamento contínuo necessário
  }
}
