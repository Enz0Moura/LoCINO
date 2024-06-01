// Arduino9x_RX
// -*- mode: C++ -*-
// Example sketch showing how to create a simple messaging client (receiver)
// with the RH_RF95 class. RH_RF95 class does not provide for addressing or
// reliability, so you should only use RH_RF95 if you do not need the higher
// level messaging abilities.
// It is designed to work with the other example Arduino9x_TX
 
#include <SPI.h>
#include <RH_RF95.h>

//#include <FileIO.h>
//#include <Console.h>

//#include <Process.h>
 
#define RFM95_CS 10
#define RFM95_RST 9
#define RFM95_INT 2
 
// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 915.0
 
// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);
 
// Blinky on receipt
#define LED 13

String dataString = "";
 
void setup() 
{
  pinMode(LED, OUTPUT);     
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  //Bridge.begin();
  //Console.begin();
  //FileSystem.begin();
 
  while (!Serial);
  Serial.begin(9600);
  //delay(100);
  
  // manual reset
  digitalWrite(RFM95_RST, LOW);
  //delay(10);
  digitalWrite(RFM95_RST, HIGH);
  //delay(10);
 
  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    while (1);
  }
 
  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }

  rf95.setTxPower(14, false);
  //rf95.setModemConfig(RH_RF95::Bw500Cr48Sf4096);
  //rf95.setModemConfig(RH_RF95::Bw500Cr45Sf128);
  //rf95.setModemConfig(RH_RF95::Bw500Cr45Sf256);
  //rf95.setModemConfig(RH_RF95::Bw500Cr45Sf512);
  //rf95.setModemConfig(RH_RF95::Bw500Cr45Sf1024);
  rf95.setModemConfig(RH_RF95::Bw125Cr45Sf128);
  //rf95.setModemConfig(RH_RF95::Bw500Cr45Sf4096);
  String title = ("Seq_Num,Date,Tmst_tx,Lat,Lng,Alt,Humid,Temp,Data,Tmst,RSSI_node,SNR");
  Serial.println(title);
}
 
void loop()
{
  //Process p;
  dataString = "";
  if (rf95.available())
  {
    // Should be a message for us now   
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);
    
    if (rf95.recv(buf, &len))
    {
      digitalWrite(LED, HIGH);
      // RH_RF95::printBuffer("Received: ", buf, len);
      // Serial.print("Got: ");
      // Serial.print((char*)buf);
      // Serial.print(",");
      // Serial.print("RSSI: ");
      // Serial.print(rf95.lastRssi(), DEC);

      dataString += String((char*)buf);
      dataString += ",";
      //dataString += getTimeStamp();
      //dataString += ",";
      dataString += rf95.lastRssi();
      dataString += ",";
      dataString += rf95.lastSNR();

      //p.runShellCommand("python /usr/lib/python2.7/tmsp.py");
      //p.run();
      Serial.println(dataString);
           
      // Send a reply
      uint8_t data[] = "And hello back to you";
      rf95.send(data, sizeof(data));
      rf95.waitPacketSent();
      //Serial.println("Sent a reply");
      digitalWrite(LED, LOW);
      
      /*File dataFile = FileSystem.open("/mnt/sdb1/datalog.csv", FILE_APPEND);

      if (dataFile) {
        dataFile.println(dataString);
        dataFile.close();
        // print to the serial port too:
        Console.println(dataString);
        //Console.println("");
      }
      else 
      {
        Console.println("error opening datalog.csv");
      }*/
      //digitalWrite(LED, LOW);
    }
    else
    {
      Serial.println("Receive failed");
    }
  }
  
  //delay(250);
}
/*
String getTimeStamp() {
  String result;
  Process time;
  // date is a command line utility to get the date and the time 
  // in different formats depending on the additional parameter 
  time.begin("date");
  time.addParameter("+%s%H");  // parameters: D for the complete date mm/dd/yy
                                //             T for the time hh:mm:ss    
  time.run();  // run the command

  // read the output of the command
  while(time.available()>0) {
    char c = time.read();
    if(c != '\n')
      result += c;
  }
  return result;
}
*/
