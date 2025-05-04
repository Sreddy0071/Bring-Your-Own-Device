# Bring Your Own Device (BYOD) Security Simulation

This project simulates a secure enterprise network that supports Bring Your Own Device (BYOD) using layered security modules like MDM, NAC, ZTNA, and Firewalls. It ensures only compliant devices get access while tracking the impact of each layer on performance metrics such as latency and throughput.

---

## 🧠 Key Concepts

- **MDM (Mobile Device Management)**: Enforces OS/encryption/jailbreak policies and adjusts device performance.
- **NAC (Network Access Control)**: Authenticates users, validates IP/port access, and assigns network segments.
- **ZTNA (Zero Trust Network Access)**: Continuously verifies device trust and revokes access if suspicious.
- **Firewall Filtering**: Allows TCP traffic, blocks UDP, and simulates dynamic packet inspection.
- **Traffic Simulation**: Uses Scapy to simulate packets from active devices.

---

## 📁 Project Structure

```
.
├── data_generation.py        # Generates realistic device data using Faker
├── mdm_module.py             # Performs MDM compliance checks
├── nac_module.py             # Enforces network access based on policies
├── ztna_module.py            # Applies ZTNA logic for trust-based access
├── firewall_module.py        # Simulates network firewall behavior
├── requirements.txt          # Dependencies
└── .gitignore                # File exclusions
```

---

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run modules in order:

```bash
python data_generation.py
python mdm_module.py
python nac_module.py
python ztna_module.py
python firewall_module.py
```

Each script reads the output from the previous step and produces updated CSV files.

---

## 📊 Outputs

- `BYOD_Device_Data.csv` → Raw device data
- `MDM_Compliant_Data.csv` → Devices passing MDM checks
- `NAC_Compliant_Data.csv` → Devices with network access
- `ZTNA_Device_Data.csv` → Trust-evaluated devices
- `Firewall_Data.csv` → Final performance post-firewall
- `Firewall_Rules_TCP_Only.csv` → Generated rule set
- `Active_Device_Traffic_Details.csv` → Simulated traffic

---

## 👩‍💻 Author

- Sowmya Reddy Likkidi  

---

## 📌 License

This project is intended for academic and educational use only. Contact the authors for permission to use in other contexts.
