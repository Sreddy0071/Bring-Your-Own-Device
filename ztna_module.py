
import pandas as pd
import numpy as np
import random

class ZTNA:
    def __init__(self):
        self.active_sessions = {}

    def authenticate(self, device):
        if device["device_id"] not in self.active_sessions:
            self.active_sessions[device["device_id"]] = "active"
            return True
        return False

    def revoke_access(self, device):
        if device["device_id"] in self.active_sessions:
            del self.active_sessions[device["device_id"]]
            print(f"Access revoked for {device['device_id']} via ZTNA.")
            return True
        return False

df_status = pd.read_csv("NAC_Compliant_Data.csv")
active_devices = df_status[df_status["Access_Status"] == "Active"]

def generate_new_status():
    return np.random.choice(["active", "revoked"], p=[0.9, 0.1])

active_devices["ZTNA_Status"] = active_devices["Device_ID"].apply(lambda _: generate_new_status())
ztna_system = ZTNA()

for index, device in active_devices.iterrows():
    device_info = {
        "device_id": device["Device_ID"],
        "ztna_status": device["ZTNA_Status"],
    }
    if device_info["ztna_status"] == "active":
        ztna_system.authenticate(device_info)
        latency_increase = random.randint(1, 5)
        active_devices.loc[index, "Latency_ms"] += latency_increase
        throughput_decrease_percent = random.randint(5, 15)
        active_devices.loc[index, "Throughput_Mbps"] *= (1 - throughput_decrease_percent / 100)
    elif device_info["ztna_status"] == "revoked":
        ztna_system.revoke_access(device_info)

active_devices.to_csv("ZTNA_Device_Data.csv", index=False)
print("ZTNA processing completed.")
