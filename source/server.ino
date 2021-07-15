#include <WiFi.h>

// personal network credentials
const char* ssid = "your_network_ssid";
const char* password = "your_network_pwd";
const uint16_t port = 80;

WiFiServer wifiServer(port); // set server port

void setup() {
  // Initialize serial
  Serial.begin(115200);
  delay(1000);
  
  // Start network connection attempt loop
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to WiFi..");
    WiFi.begin(ssid, password);
    delay(1000);
  }
  // Successful connection
  Serial.println("Connected to the WiFi network");
  Serial.println(WiFi.localIP()); // print ESP32 IP in local network
  wifiServer.begin(); // start server
}

void loop() {
  WiFiClient client = wifiServer.available(); // listen for clients
  if(client){ // check if client is connected and then exchange data
    Serial.println("Status: Client available. \nEngaging connection...");
    while(client.connected()){ // mantain until stop the connection
      while(client.available()>0){ // check if client sent data (#bytes>0)
        uint32_t sizeRnd = client.readString().toInt(); // transform desired size from string to int
        for(unsigned itr=0; itr<sizeRnd; itr++){client.println(esp_random());} // send data
      }
      delay(10);
    }
    // stop connection with client
    client.stop();
    Serial.println("Client disconnected");
  } else{
    delay(1000);
    Serial.println("Status: IDLE.");
  }
}
