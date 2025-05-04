
import pandas as pd
import ipaddress
import random

class Device:
    def __init__(self, device_id, device_type, is_compliant, user_role, destination, ip_address, port, Latency_ms, Throughput_Mbps, access_code=None):
        self.device_id = device_id
        self.device_type = device_type
        self.is_compliant = is_compliant
        self.user_role = user_role.lower()
        self.destination = destination.lower()
        self.ip_address = ip_address
        self.port = port
        self.access_granted = False
        self.assigned_resource = None
        self.vlan_segment = None
        self.latency_ms = Latency_ms
        self.throughput_Mbps = Throughput_Mbps
        self.access_code = access_code
        self.access_status = "Access Denied"

class NACSystem:
    def __init__(self, allowed_ip_range, secure_ports):
        self.allowed_roles = ["employee", "admin"]
        self.allowed_destinations = {
            "network": "Corporate Network Resources",
            "app": "Internal Applications",
            "cloud": "Cloud Storage Services",
        }
        self.network_segments = {
            "employee": "VLAN 100 - Employee Network",
            "admin": "VLAN 200 - Admin Network",
            "end-guest": "Guest Network",
        }
        self.guest_access_code = "NETGUEST"
        self.allowed_ip_network = ipaddress.ip_network(allowed_ip_range)
        self.secure_ports = secure_ports

    def authenticate_device(self, device):
        if device.user_role == "end-guest":
            return device.access_code == self.guest_access_code
        elif device.user_role in self.allowed_roles:
            return True
        return False

    def check_ip_address(self, ip_address):
        try:
            device_ip = ipaddress.ip_address(ip_address)
            return device_ip in self.allowed_ip_network
        except ValueError:
            return False

    def check_port(self, port):
        return port in self.secure_ports

    def enforce_access_policy(self, device):
        if not self.authenticate_device(device):
            return
        if device.user_role in self.allowed_roles and device.destination in self.allowed_destinations:
            if self.check_ip_address(device.ip_address) and self.check_port(device.port):
                device.assigned_resource = self.allowed_destinations[device.destination]
                device.vlan_segment = self.network_segments[device.user_role]
                device.access_granted = True
                device.access_status = "Active"
        elif device.user_role == "end-guest" and device.destination == "network":
            device.assigned_resource = self.network_segments["end-guest"]
            device.access_granted = True
            device.access_status = "Active"

    def process_device(self, device):
        if not device.is_compliant:
            device.access_status = "Non-Compliant"
            return
        self.enforce_access_policy(device)

if __name__ == "__main__":
    df = pd.read_csv("MDM_Compliant_Data.csv")
    compliant_devices_df = df[df["Compliance_Status"] == "Compliant"].copy()
    compliant_devices_df.drop(columns=["Non_Compliance_Reason"], inplace=True)
    allowed_ip_range = "192.168.1.0/24"
    secure_ports = [443, 8443]
    nac_system = NACSystem(allowed_ip_range, secure_ports)

    devices = []
    access_status_list = []

    for _, row in compliant_devices_df.iterrows():
        access_code = "NETGUEST" if row["Role"].lower() == "end-guest" else None
        device = Device(
            device_id=row["Device_ID"],
            device_type=row["Device_Type"],
            is_compliant=True,
            user_role=row["Role"],
            destination=row["Destination_Type"],
            ip_address=row["IP_Address"],
            port=row["Port"],
            Latency_ms=row["Latency_ms"],
            Throughput_Mbps=row["Throughput_Mbps"],
            access_code=access_code,
        )
        devices.append(device)
        nac_system.process_device(device)
        access_status_list.append({"Device_ID": device.device_id, "Access_Status": device.access_status})

    status_df = pd.DataFrame(access_status_list)
    updated_compliant_df = compliant_devices_df.merge(status_df, on="Device_ID")
    updated_compliant_df.to_csv("NAC_Compliant_Data.csv", index=False)
    print("Processed NAC compliance and saved.")
