import urequests as requests
import network
from time import sleep
from machine import I2C, Pin
from VEML6030 import VEML6030

# Wi-Fi credentials
SSID = "102679553159"
PASSWORD = "Angel@123"

# Firebase Realtime Database URL with .json at the end
firebase_url = "https://spartan-concord-413207-default-rtdb.asia-southeast1.firebasedatabase.app/sensor_data.json"

# Initialize I2C and VEML6030 sensor
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000)
sensor = VEML6030(i2c)

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print("Connecting to Wi-Fi...")
    sleep(1)
print("Connected to Wi-Fi:", wlan.ifconfig())

# Function to send sensor data to Firebase
def send_data_to_firebase(lux_value):
    # Data payload to send
    data = {
        "lux": lux_value
    }
    
    try:
        # Send POST request to Firebase
        response = requests.post(firebase_url, json=data)
        
        if response.status_code == 200:
            print("Data sent successfully!")
        else:
            print(f"Failed to send data: {response.status_code}, {response.text}")
        
        response.close()
    except Exception as e:
        print("Error sending data:", e)

# Main loop to read sensor data and send it to Firebase
try:
    while True:
        # Read lux value from the sensor
        lux_value = sensor.read()
        print(f"Lux: {lux_value}")
        
        # Send lux value to Firebase
        send_data_to_firebase(lux_value)
        
        sleep(1)  # Delay between readings
except KeyboardInterrupt:
    print("Stopped reading sensor.")


