/*  ___   ___  ___  _   _  ___   ___   ____ ___  ____  
 * / _ \ /___)/ _ \| | | |/ _ \ / _ \ / ___) _ \|    \ 
 *| |_| |___ | |_| | |_| | |_| | |_| ( (__| |_| | | | |
 * \___/(___/ \___/ \__  |\___/ \___(_)____)___/|_|_|_|
 *                  (____/ 
 * Osoyoo Wifi Smart Home V2.0 udp project Lesson 2-5
 * 
 * tutorial url: https://osoyoo.com/?p=46326
 */
#include <WiFiEsp.h>
#include "OsoyooIOT.h"

int servoPin = 11;//servo connect to D11
#include <Wire.h> 
String marystr="33cd216fb"; //change 33cd216fb with the your test ID card  
String davidstr="***";       //change *** with the your test 2nd ID card  
char ssid[] = "***";//replace *** with your wifi ssid
char pass[] = "***"; //replace *** with your wifi password
#include <SoftwareSerial.h>
SoftwareSerial softserial(A9, A8); // RX, TX
#include <SPI.h>
#include <RFID.h>
RFID rfid(48,49);   //SDA,RST

int LED = 2;      //LED connects to D2
int Button = 3;   //button connects to D3

bool state=true;
int status = WL_IDLE_STATUS;     // the Wifi radio's status

unsigned int localPort = 8888;  // local port to listen on

char packetBuffer[255];          // buffer to hold incoming packet
 
IPAddress remoteIp=IPAddress(192,168,1,255);//if your Arduino IP is sth like 192.168.0.xx set this value to 192.168.0.255
IPAddress localip;
OsoyooIOT udp;


void setup() {

  pinMode(LED,OUTPUT);
  pinMode(Button,INPUT);
  Serial.begin(9600);

  pinMode(servoPin, OUTPUT);
 
  pinMode(LED, OUTPUT);
  digitalWrite(LED,LOW);
  Serial.begin(9600);   // initialize serial for debugging

  softserial.begin(115200);
  softserial.write("AT+CIOBAUD=9600\r\n");
  softserial.write("AT+RST\r\n");
  softserial.begin(9600);    // initialize serial for ESP module

  WiFi.init(&softserial);    // initialize ESP module
  SPI.begin(); 
  rfid.init();
  
  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue:
    while (true);
  }

  // attempt to connect to WiFi network
  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network
    status = WiFi.begin(ssid, pass);
  }

  Serial.println("Connected to wifi");
  printWifiStatus();

  Serial.println("\nStarting connection to server...");
  // if you get a connection, report back via serial:
  udp.begin(localPort);

  Serial.print("Listening on port ");
  Serial.println(localPort);
 
}

void loop()
{
 
  int buttonState = digitalRead(Button);
  if (buttonState == LOW) {
    Serial.println("Door is OPEN by button!");
    opendoor();  
  }
 
 
  unsigned char type[MAX_LEN];
  //Find the card
  if (rfid.isCard( )) 
  {
    Serial.println("Find the card!");
    // Show card type
    ShowCardType(type);
    if (rfid.readCardSerial())
    { String rfidstr=String(rfid.serNum[0],HEX)+String(rfid.serNum[1],HEX)+String(rfid.serNum[2],HEX)+String(rfid.serNum[3],HEX)+String(rfid.serNum[4],HEX);
      Serial.print("The card’s number is  : ");
      Serial.println(rfidstr);
 
      ShowUser(rfidstr);
    }
    //Select card, return card capacity (lock card, prevent most read), remove the line to read the card continuously
    Serial.println(rfid.selectTag(rfid.serNum));
  }

  rfid.halt();

 
  udp.loop();
  if(udp.available()){
    Serial.print("Received packet of size ");
    Serial.print(udp.packetSize());
    remoteIp = udp.remoteIP();
    OsoyooCommand myData = udp.read();
    Serial.print(" Command:");
    String command = String(myData.command);
    Serial.print(command);
    
    String ipstr="Arduino in "+ String(localip[0])+"."+String(localip[1])+"."+String(localip[2])+"."+String(localip[3])+" is connected\n";
    int str_len = ipstr.length() + 1; 
    char udp_array[str_len];
    ipstr.toCharArray(udp_array, str_len);
    Serial.print(" from ");
    Serial.println(remoteIp);
    udp.beginPacket(remoteIp,8888); // send reply packet to port 8888
    udp.write(udp_array, sizeof(udp_array)-1); 
    udp.endPacket();
    if(command=="O") {
     
      char msg[]="Door is open by APP!\n";
      Serial.println(msg);
      udp.beginPacket(remoteIp,8888); // send reply packet to port 8888
      udp.write(msg, sizeof(msg)-1); 
      udp.endPacket();
      opendoor();
    }
  }


}

void ShowCardType( unsigned char* type)
{
  Serial.print("Card type: ");
  if(type[0]==0x04&&type[1]==0x00) Serial.println("MFOne-S50");
  else if(type[0]==0x02&&type[1]==0x00) Serial.println("MFOne-S70");
    else if(type[0]==0x44&&type[1]==0x00) Serial.println("MF-UltraLight");
      else if(type[0]==0x08&&type[1]==0x00) Serial.println("MF-Pro");
        else if(type[0]==0x44&&type[1]==0x03) Serial.println("MF Desire");
          else  Serial.println("Unknown");
}
void ShowUser( String rfidstr)
{
  //32 DA 94 10 6C
  if( rfidstr==marystr) {
    char msg[]="Mary at the door!\n";
    Serial.println(msg);
    udp.beginPacket(remoteIp,8888); // send reply packet to port 8888
    udp.write(msg, sizeof(msg)-1); 
    udp.endPacket();
    opendoor();
  }
  else if(rfidstr==davidstr) 
  {
    char msg[]="David at the door!\n";
    Serial.println(msg);
    udp.beginPacket(remoteIp,8888); // send reply packet to port 8888
    udp.write(msg, sizeof(msg)-1); 
    udp.endPacket();
    opendoor();
  }
  else
  {
      String msg=rfidstr+" ID is unknown\n";
      int str_len = msg.length() + 1; 
      char udp_array[str_len];
      msg.toCharArray(udp_array, str_len);
      Serial.print(msg);
      digitalWrite(LED, HIGH);   // turn the LED on (HIGH is the voltage level)
      udp.beginPacket(remoteIp,8888); // send reply packet to port 8888
      udp.write(udp_array, sizeof(udp_array)-1); 
      udp.endPacket();
  }
}

void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  localip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(localip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}
void opendoor(){
      digitalWrite(LED, HIGH);   // turn the LED on (HIGH is the voltage level)
      for(int i=0;i<50;i++){
        int pulsewidth = (0 * 11) + 500; //
        digitalWrite(servoPin, HIGH);   //
        delayMicroseconds(pulsewidth);  //
        digitalWrite(servoPin, LOW);    //
        delayMicroseconds(20000 - pulsewidth);
      }
      delay(2000);
      Serial.println("Close the door");
      for(int i=0;i<50;i++){
        int pulsewidth = (110 * 11) + 500; //
        digitalWrite(servoPin, HIGH);   //
        delayMicroseconds(pulsewidth);  //
        digitalWrite(servoPin, LOW);    //
        delayMicroseconds(20000 - pulsewidth);
      }
      digitalWrite(LED, LOW);    // turn the LED off by making the voltage LOW
      delay(1000);
}
