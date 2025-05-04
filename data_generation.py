
# Data Generation and Initialization
import pandas as pd
import numpy as np
import random
from faker import Faker

faker = Faker()
num_devices = 100

def generate_mac():
    return faker.mac_address()

def generate_os(device_type):
    if device_type == "Laptop":
        os_types = {
            "Windows": ["10", "11"],
            "macOS": ["Monterey", "Ventura"],
            "Linux": ["Ubuntu 20.04", "Fedora 36", "Debian 11"],
        }
    elif device_type in ["Smartphone", "Tablet"]:
        os_types = {
            "Android": ["12", "13"],
            "iOS": ["15", "16"],
        }
    else:
        return "Unknown OS"
    os_choice = random.choice(list(os_types.keys()))
    version = random.choice(os_types[os_choice])
    return f"{os_choice} {version}"

def generate_port():
    ports = [443, 8443, 80, 8080, 22, 21, 25, 3389]
    probabilities = [0.5, 0.3, 0.05, 0.05, 0.03, 0.03, 0.02, 0.02]
    return random.choices(ports, probabilities)[0]

def generate_device_data(num_devices=100):
    device_data = {
        "Device_ID": [f"Device_{i+1}" for i in range(num_devices)],
        "MAC_Address": [generate_mac() for _ in range(num_devices)],
        "Device_Type": np.random.choice(["Laptop", "Smartphone", "Tablet"], size=num_devices),
        "Role": np.random.choice(["End-Guest", "Employee", "Administrator"], size=num_devices, p=[0.1, 0.7, 0.2]),
        "Destination_Type": np.random.choice(["Network", "App", "Cloud"], size=num_devices),
        "Timestamp": [faker.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S") for _ in range(num_devices)],
        "Encryption_Type": np.random.choice(["AES", "DSA", "ECC", "RSA"], size=num_devices, p=[0.45, 0.05, 0.45, 0.05]),
        "Jailbreak_Status": np.random.choice(["Yes", "No"], size=num_devices, p=[0.1, 0.9]),
        "Latency_ms": np.random.normal(50, 10, size=num_devices).round(2),
        "Throughput_Mbps": np.random.normal(100, 15, size=num_devices).round(2),
        "Port": [generate_port() for _ in range(num_devices)],
        "IP_Address": [f"192.168.1.{random.randint(0, 255)}" if random.random() < 0.95 else faker.ipv4() for _ in range(num_devices)],
        "Screen_Time": np.random.choice(["1", "5", "10", "30", "60"], size=num_devices, p=[0.05, 0.3, 0.55, 0.05, 0.05]),
    }
    device_data["OS_Version"] = [generate_os(device_type) for device_type in device_data["Device_Type"]]
    df = pd.DataFrame(device_data)
    df.to_csv("BYOD_Device_Data.csv", index=False)
    return df

if __name__ == "__main__":
    df = generate_device_data(num_devices)
    print(df.head())
