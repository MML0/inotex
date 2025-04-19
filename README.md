# INOTEX Interactive System

A comprehensive interactive system combining ESP8266 microcontrollers, LED control, physical switches, and web streaming capabilities, designed for interactive installations and performances.

## System Components

### 1. LED Control Module
- **Hardware**: ESP8266 + WS2812 LED strips
- **Features**:
  - Real-time LED control via TouchDesigner
  - UDP communication protocol
  - Support for multiple LED patterns and animations
  - Low latency response for live performances

### 2. Switch Module
- **Hardware**: ESP8266 + Microswitches
- **Features**:
  - 8-switch input support
  - Long press detection
  - Real-time state transmission to TouchDesigner
  - UDP communication protocol (Port 4210)
  - Switch state monitoring and event handling

### 3. Stream Module
- **Features**:
  - TouchDesigner to Android browser streaming
  - Real-time video/graphics transmission
  - Web-based viewer interface
  - Cross-platform compatibility

## Setup Instructions

### LED Module Setup
1. Flash the ESP8266 with the LED control firmware
2. Connect WS2812 LED strip to ESP8266:
   - Data pin: GPIO2 (D4)
   - Power: 5V
   - Ground: GND
3. Configure WiFi settings in the ESP code
4. Set up TouchDesigner with UDP output

### Switch Module Setup
1. Flash ESP8266 with the switch firmware
2. Connect microswitches:
   - Switch inputs: GPIO pins as configured
   - Common ground connection
3. Update UDP_IP in receiver.py to match your computer's IP
4. Run the Python receiver script to capture switch states

### Stream Setup
1. Configure TouchDesigner output settings
2. Set up web server for stream delivery
3. Access stream via Android browser using provided URL

## Network Configuration
- Default Switch Module Port: 4210
- Ensure all devices are on the same network
- Configure firewalls to allow UDP communication

## Dependencies
- ESP8266 Arduino Core
- FastLED library for WS2812
- Python 3.x for receiver script
- TouchDesigner (compatible version)

## Usage
1. Power up ESP8266 modules
2. Launch TouchDesigner project
3. Start Python receiver script
4. Initialize web stream if needed
5. System is ready for interactive control

## Troubleshooting
- Check network connectivity between devices
- Verify IP addresses and port configurations
- Ensure proper power supply for LED strips
- Monitor serial output for ESP8266 debugging

## Contributing
Feel free to contribute to this project by submitting issues or pull requests.

## License
This project is open-source and available under the MIT License.

https://github.com/FiloSottile/mkcert

https://touchdesigner.github.io/WebRTC-Remote-Panel-Web-Demo/

https://github.com/TouchDesigner/WebRTC-Remote-Panel-Web-Demo

https://forum.derivative.ca/t/webrtc-dat-tutorial/255218



