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

void setup() {
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

void loop() {
  if (Serial.available() >= 32) { // Esperar até que todos os bytes da mensagem sejam recebidos
    uint8_t received_message[32];
    Serial.readBytes(received_message, 32);
    
    // Enviar a mensagem via LoRa
    Serial.print("Enviando mensagem: ");
    for (uint8_t i = 0; i < sizeof(received_message); i++) {
      Serial.print(received_message[i], HEX);
      Serial.print(" ");
    }
    Serial.println();

    rf95.send(received_message, sizeof(received_message));
    rf95.waitPacketSent();
  }

  delay(1000); // Aguardar um pouco antes de verificar novamente
}
