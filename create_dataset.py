import pandas as pd
import random
import numpy as np

# Parameters for the dataset
num_packets = 1000  # Total number of packets
attack_duration = 300  # Number of attack packets
normal_duration = num_packets - attack_duration

# Helper functions
def generate_ip():
    """Generate a random IP address."""
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# Generate normal traffic
data = {
    "timestamp": pd.date_range(start="2024-11-21 00:00:00", periods=num_packets, freq="s"),
    "source_ip": [generate_ip() for _ in range(normal_duration)] + ["192.168.1.1"] * attack_duration,
    "destination_ip": [generate_ip() for _ in range(num_packets)],
    "protocol": random.choices(["TCP", "UDP", "ICMP"], weights=[70, 25, 5], k=normal_duration)
               + ["TCP"] * attack_duration,
    "packet_size": [random.randint(40, 1500) for _ in range(normal_duration)]
                  + [random.randint(800, 1500)] * attack_duration,
    "packet_count": [1] * normal_duration + [random.randint(50, 200)] * attack_duration
}

# Combine into a DataFrame
df = pd.DataFrame(data)

# Add attack flags
df["attack_flag"] = [0] * normal_duration + [1] * attack_duration

# Shuffle the dataset
df = df.sample(frac=1).reset_index(drop=True)

# Save to CSV
df.to_csv("datasets/dos_attack_dataset.csv", index=False)

print("Synthetic DoS attack dataset created successfully!")
