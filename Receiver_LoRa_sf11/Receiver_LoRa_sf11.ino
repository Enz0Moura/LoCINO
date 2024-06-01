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

  // Envia uma mensagem indicando que está pronto para receber dados
  Serial.println("READY");
}

void loop()
{
  if (rf95.available()) {
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);

    if (rf95.recv(buf, &len)) {
      Serial.print("Mensagem recebida: ");
      for (uint8_t i = 0; i < len; i++) {
        Serial.print(buf[i], HEX);
        Serial.print(" ");
      }
      Serial.println();
      
      // Verifique se a mensagem contém o cabeçalho esperado
      if (buf[0] == 0xFF && buf[1] == 0xFF) {
        Serial.println("Cabeçalho verificado");

        // Transmite os dados recebidos de volta para o Python para desserialização
        Serial.write(buf, len);
      } else {
        Serial.println("Cabeçalho incorreto");
      }
    } else {
      Serial.println("Falha na recepção");
    }
  }
  delay(250);
}
