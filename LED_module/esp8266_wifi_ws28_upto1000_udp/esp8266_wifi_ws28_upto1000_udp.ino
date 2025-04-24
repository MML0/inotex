#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <FastLED.h>

#define LED_PIN D2  // Pin connected to the data line of the WS2812B
#define NUM_LEDS 1024  // Total number of LEDs in the strip
#define LED_TYPE WS2812B
#define COLOR_ORDER GRB

CRGB leds[NUM_LEDS];
uint8_t Data[NUM_LEDS * 3];
unsigned long lastDataTime = 0;  // To track last data reception time
const unsigned long ledOffDelay = 2000; // 10 seconds timeout to turn off LEDs

const byte specialSequence[10] = {0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A};
bool specialSequenceReceived = false;
int shiftSpeed = 0;  // Default shifting speed
int lastShiftSpeed = 0;

const char* ssid = "."; // Replace with your network SSID
const char* password = "12345678an";           // Replace with your network password
const IPAddress staticIP(192, 168, 0, 118);   // Static IP for the ESP8266
const IPAddress gateway(192, 168, 0, 1);      // Default gateway
const IPAddress subnet(255, 255, 255, 0);      // Subnet mask

unsigned int localPort = 8266;  // Local port to listen for UDP packets
WiFiUDP udp;
void setup() {
  Serial.begin(115200);
  
  WiFi.config(staticIP, gateway, subnet);
  WiFi.begin(ssid, password);

  Serial.println(".");
  Serial.println("connecting...");

  while (WiFi.status() != WL_CONNECTED ) {
    delay(500);
    Serial.print(".");
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected");
    Serial.print("ESP IP Address: ");
    Serial.println(WiFi.localIP());
    
    // Start UDP only if WiFi is connected
    udp.begin(localPort);
    Serial.printf("Listening for UDP packets on port %d\n", localPort);
  } else {
    Serial.println("\nWiFi connection failed! Running in offline mode.");
  }

  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(255);

  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.show();


}

void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    lastDataTime = millis(); // Reset timeout timer
    
    byte startByte = udp.read();
    
    // Check for sync byte (0xAA)
    if (startByte == 0xAA) {   
      udp.read(Data, NUM_LEDS * 3);  // Read RGB data

      // Process RGB data if no special sequence is found
      for (int i = 0; i < NUM_LEDS; i++) {
        byte r = Data[i * 3];
        byte g = Data[i * 3 + 1];
        byte b = Data[i * 3 + 2];
        leds[i] = CRGB(r, g, b);  // Set color for LED
      }

      FastLED.show();
      
    }
  }

  // If no data is received for 10 seconds, turn off the LEDs
  if (millis() - lastDataTime > ledOffDelay ) {
    lastDataTime = millis(); // Reset timeout timer
    fill_solid(leds, NUM_LEDS, CRGB::Black);
    FastLED.show();
  }

}
