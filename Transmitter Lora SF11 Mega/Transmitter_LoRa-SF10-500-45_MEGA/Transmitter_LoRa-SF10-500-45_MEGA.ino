#include <SPI.h>
#include <RH_RF95.h>

#define RFM95_CS 10
#define RFM95_RST 9
#define RFM95_INT 2
#define RF95_FREQ 915.0

RH_RF95 rf95(RFM95_CS, RFM95_INT);

struct Message {
  unsigned int message_type: 1;
  unsigned int id: 15;
  unsigned long latitude: 24;
  unsigned long longitude: 24;
  unsigned int group_flag: 1;
  unsigned int record_time: 16;
  unsigned int max_records: 11;
  unsigned int hop_count: 4;
  unsigned int channel: 2;
  unsigned int location_time: 16;
  unsigned int help_flag: 2;
  unsigned int battery: 4;
};

void setup() 
{
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);
  Serial.begin(9600);

  while (!Serial);
  delay(100);

  Serial.println("Iniciando LoRa...");

  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  if (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    while (1);
  } else {
    Serial.println("LoRa radio init successful");
  }

  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  } else {
    Serial.println("setFrequency successful");
  }

  rf95.setTxPower(14, false);
  rf95.setModemConfig(RH_RF95::Bw125Cr45Sf128);
  Serial.println("Setup completo");
}

void loop()
{
  // Criar e preencher a mensagem
  Message message;
  message.message_type = 1;
  message.id = 1;
  message.latitude = 0x50D1F0; // Exemplo de coordenada 50.1234
  message.longitude = 0x081F36; // Exemplo de coordenada 8.1234
  message.group_flag = 0;
  message.record_time = 12345;
  message.max_records = 2047;
  message.hop_count = 15;
  message.channel = 3;
  message.location_time = 6789;
  message.help_flag = 2;
  message.battery = 15;

  // Serializar a mensagem em um buffer de bytes
  uint8_t buf[21];
  buf[0] = 0xFF;
  buf[1] = 0xFF;
  buf[2] = (message.message_type & 0x01) | ((message.id >> 7) & 0xFE);
  buf[3] = message.id & 0x7F;
  buf[4] = (message.latitude >> 16) & 0xFF;
  buf[5] = (message.latitude >> 8) & 0xFF;
  buf[6] = message.latitude & 0xFF;
  buf[7] = (message.longitude >> 16) & 0xFF;
  buf[8] = (message.longitude >> 8) & 0xFF;
  buf[9] = message.longitude & 0xFF;
  buf[10] = message.group_flag & 0x01;
  buf[11] = (message.record_time >> 8) & 0xFF;
  buf[12] = message.record_time & 0xFF;
  buf[13] = (message.max_records >> 8) & 0x07;
  buf[14] = message.max_records & 0xFF;
  buf[15] = ((message.hop_count & 0x0F) << 4) | (message.channel & 0x03);
  buf[16] = (message.location_time >> 8) & 0xFF;
  buf[17] = message.location_time & 0xFF;
  buf[18] = ((message.help_flag & 0x03) << 6) | (message.battery & 0x0F);

  // Enviar a mensagem
  rf95.send(buf, sizeof(buf));
  rf95.waitPacketSent();

  Serial.println("Mensagem enviada");

  delay(10000); // Envia a cada 10 segundos
}
