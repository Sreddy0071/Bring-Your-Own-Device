
import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt

df = pd.read_csv("BYOD_Device_Data.csv")

def check_compliance(row):
    reasons = []
    os_policy = {
        "Windows": ["10", "11"],
        "macOS": ["Monterey", "Ventura"],
        "Android": ["12", "13"],
        "iOS": ["15", "16"],
        "Linux": ["Ubuntu 20.04", "Fedora 36", "Debian 11"],
    }
    os_type, os_version = row["OS_Version"].split(" ", 1)
    if os_type in os_policy and os_version not in os_policy[os_type]:
        reasons.append(f"OS version {row['OS_Version']} not compliant")
    if row["Encryption_Type"] not in ["AES", "ECC"]:
        reasons.append(f"Encryption standard {row['Encryption_Type']} not compliant")
    if row["Jailbreak_Status"] == "Yes":
        reasons.append("Device is jailbroken")
    if int(row["Screen_Time"]) > 10:
        reasons.append("Screen time exceeded 10 minutes and was adjusted to comply with policy")
    if not reasons:
        return "Compliant", ""
    return "Non-Compliant", "; ".join(reasons)

df["Compliance_Status"], df["Non_Compliance_Reason"] = zip(*df.apply(check_compliance, axis=1))

def adjust_performance_random(row):
    if row["Compliance_Status"] == "Compliant":
        latency_increase = random.randint(1, 5)
        row["Latency_ms"] += latency_increase
        throughput_decrease_percent = random.randint(1, 10)
        row["Throughput_Mbps"] *= (1 - throughput_decrease_percent / 100)
    return row

df = df.apply(adjust_performance_random, axis=1)
df.to_csv("MDM_Compliant_Data.csv", index=False)
print(df.head())

latency_avg = df["Latency_ms"].mean()
throughput_avg = df["Throughput_Mbps"].mean()
print(f"Average Latency: {latency_avg:.2f} ms")
print(f"Average Throughput: {throughput_avg:.2f} Mbps")
