#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

// Wi-Fi credentials
const char* ssid = "."; // Replace with your network SSID
const char* password = "12345678an";           // Replace with your network password

// Network configuration
IPAddress staticIP(192, 168, 43, 12);   // Static IP for the ESP8266
IPAddress gateway(192, 168, 43, 1);      // Default gateway
IPAddress subnet(255, 255, 255, 0);      // Subnet mask

// UDP
WiFiUDP udp;
const char* udpAddress = "192.168.43.81";     // Replace with the destination IP (Python script's IP)
const int udpPort = 4210;                      // Replace with the destination port

// Pins
const int digitalPins[] = {16, 14, 12, 13, 15, 4, 0, 2}; // Adjust the digital pins to ESP8266 GPIO pins
const int numDigitalPins = sizeof(digitalPins) / sizeof(digitalPins[0]);

// Buffers
uint8_t dataBuffer[numDigitalPins]; // Adjusted buffer size for digital pins only
uint8_t previousStates[numDigitalPins]; // Buffer to store previous states of pins

// Timing
unsigned long lastSendTime = 0; // Stores the last time data was sent
const unsigned long sendInterval = 5; // Minimum interval for sending data (in milliseconds)

// Function to connect to Wi-Fi
void connectToWiFi() {
  WiFi.config(staticIP, gateway, subnet);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi!");
}

void setup() {
  // Initialize Serial
  Serial.begin(115200);

  // Connect to Wi-Fi
  connectToWiFi();

  // Initialize pins and previous states
  for (int i = 0; i < numDigitalPins; i++) {
    pinMode(digitalPins[i], INPUT_PULLUP);
    previousStates[i] = digitalRead(digitalPins[i]); // Initialize with the current state
  }

  // Start UDP
  udp.begin(udpPort);
  Serial.println("UDP started!");
}

void loop() {
  bool stateChanged = false; // Flag to track if any state has changed

  // Check digital pins for changes
  for (int i = 0; i < numDigitalPins; i++) {
    uint8_t currentState = digitalRead(digitalPins[i]);
    if (currentState != previousStates[i]) { // Check for a change
      stateChanged = true;
      previousStates[i] = currentState; // Update previous state
    }
    dataBuffer[i] = currentState; // Update the buffer
  }

  // Only send data if a state has changed and enough time has elapsed
  unsigned long currentTime = millis();
  if (stateChanged && (currentTime - lastSendTime > sendInterval)) {
    lastSendTime = currentTime; // Update the last send time

    // Print data to Serial
    Serial.print("State Changed. Data Buffer: ");
    for (int i = 0; i < numDigitalPins; i++) {
      Serial.print(dataBuffer[i]);
      Serial.print(" ");
    }
    Serial.println();

    // Send data over UDP
    udp.beginPacket(udpAddress, udpPort);
    udp.write(dataBuffer, sizeof(dataBuffer));
    udp.endPacket();
  }
}
