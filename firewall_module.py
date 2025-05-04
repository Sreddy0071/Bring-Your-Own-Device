
import pandas as pd
import random
from scapy.all import Ether, IP, TCP, UDP

df = pd.read_csv("ZTNA_Device_Data.csv")

def generate_traffic(device_data):
    packets = []
    for _, row in device_data.iterrows():
        if row["Access_Status"] == "Active":
            ip_src = row["IP_Address"]
            mac_src = row["MAC_Address"]
            port = row["Port"]
            device_id = row["Device_ID"]
            timestamp = row["Timestamp"]
            latency = row["Latency_ms"]
            throughput = row["Throughput_Mbps"]
            dest_port = port if port in [443, 8443] else random.choice([443, 8443])
            dest_ip = f"10.0.{random.randint(0, 255)}.{random.randint(1, 255)}"
            packet_type = random.choice([TCP, UDP])
            packet = Ether(src=mac_src)/IP(src=ip_src, dst=dest_ip)/packet_type(dport=dest_port)
            packets.append({
                "Device_ID": device_id,
                "Source_MAC": mac_src,
                "Source_IP": ip_src,
                "Destination_IP": dest_ip,
                "Protocol": "TCP" if packet_type == TCP else "UDP",
                "Destination_Port": dest_port,
                "Timestamp": timestamp,
                "Latency_ms": latency,
                "Throughput_Mbps": throughput
            })
    traffic_df = pd.DataFrame(packets)
    traffic_df.to_csv("Active_Device_Traffic_Details.csv", index=False)
    print("Traffic data saved.")

def generate_tcp_only_firewall_rules(traffic_data):
    firewall_rules = []
    for _, row in traffic_data.iterrows():
        if row["Protocol"] == "TCP":
            firewall_rules.append({
                "Action": "ALLOW",
                "Source_MAC": row["Source_MAC"],
                "Source_IP": row["Source_IP"],
                "Destination_IP": row["Destination_IP"],
                "Protocol": row["Protocol"],
                "Destination_Port": row["Destination_Port"]
            })
    firewall_rules.append({
        "Action": "DENY",
        "Source_MAC": "*",
        "Source_IP": "*",
        "Destination_IP": "*",
        "Protocol": "UDP",
        "Destination_Port": "*"
    })
    rules_df = pd.DataFrame(firewall_rules)
    rules_df.to_csv("Firewall_Rules_TCP_Only.csv", index=False)
    print("Firewall rules saved.")
    return rules_df

def adjust_latency_throughput(row):
    if row["Protocol"] == "TCP":
        row["Latency_ms"] += random.randint(5, 15)
        row["Throughput_Mbps"] *= (1 - random.randint(10, 25) / 100)
    return row

generate_traffic(df)
traffic_df = pd.read_csv("Active_Device_Traffic_Details.csv")
firewall_rules_df = generate_tcp_only_firewall_rules(traffic_df)
traffic_df = traffic_df.apply(adjust_latency_throughput, axis=1)
traffic_df.to_csv("Firewall_Data.csv", index=False)
print("Firewall data saved.")
