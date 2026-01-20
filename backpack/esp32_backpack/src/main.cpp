#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "CloneTrooper-HUD";
const char* password = "Order66Execute";

// MQTT
const char* mqtt_server = "192.168.4.1";
WiFiClient espClient;
PubSubClient client(espClient);

// TODO: Sensor objects
// - BNO055
// - ENS160
// - AHT21
// - BME280
// - INA219

void setup_wifi() {
    Serial.println("Connecting to WiFi...");
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    Serial.println("\nWiFi connected");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
}

void reconnect_mqtt() {
    while (!client.connected()) {
        Serial.print("Connecting to MQTT...");
        if (client.connect("ESP32_Helmet")) {
            Serial.println("connected");
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" retrying in 5s");
            delay(5000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    Serial.println("ESP32 Helmet - Starting");
    
    // Initialize I2C
    Wire.begin();
    
    // Connect WiFi
    setup_wifi();
    
    // Setup MQTT
    client.setServer(mqtt_server, 1883);
    
    // TODO: Initialize sensors
    
    Serial.println("Setup complete");
}

void loop() {
    if (!client.connected()) {
        reconnect_mqtt();
    }
    client.loop();
    
    // TODO: Read sensors
    // TODO: Publish to MQTT
    
    delay(1000);
}
