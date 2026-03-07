import json
import os

data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'seed_data.json')

with open(data_path, 'r') as f:
    data = json.load(f)

# Add new CPUs
new_cpus = [
    {
        "id": "cpu_030",
        "name": "Intel Core Ultra 9 285K",
        "brand": "Intel",
        "socket": "LGA1851",
        "cores": 24,
        "threads": 24,
        "base_clock": 3.7,
        "boost_clock": 5.7,
        "tdp": 125,
        "performance_score": 105,
        "gaming_score": 95,
        "price": 60000,
        "supported_ram": ["DDR5"],
        "integrated_graphics": True,
        "igpu_name": "Intel Graphics",
        "category": "enthusiast"
    },
    {
        "id": "cpu_031",
        "name": "AMD Ryzen 9 9950X3D",
        "brand": "AMD",
        "socket": "AM5",
        "cores": 16,
        "threads": 32,
        "base_clock": 4.1,
        "boost_clock": 5.7,
        "tdp": 162,
        "performance_score": 106,
        "gaming_score": 115,
        "price": 68000,
        "supported_ram": ["DDR5"],
        "integrated_graphics": False,
        "category": "enthusiast"
    }
]

# Add new GPUs
new_gpus = [
    {
        "id": "gpu_020",
        "name": "NVIDIA GeForce RTX 4070 Ti SUPER",
        "brand": "NVIDIA",
        "vram": 16,
        "vram_type": "GDDR6X",
        "tdp": 285,
        "length_mm": 310,
        "performance_score": 87,
        "price": 75000,
        "category": "high-end",
        "ray_tracing": True,
        "dlss_version": 3
    },
    {
        "id": "gpu_021",
        "name": "AMD Radeon RX 7900 GRE",
        "brand": "AMD",
        "vram": 16,
        "vram_type": "GDDR6",
        "tdp": 260,
        "length_mm": 280,
        "performance_score": 85,
        "price": 55000,
        "category": "high-end",
        "ray_tracing": True,
        "fsr_version": 3
    }
]

# Append items if they don't already exist
existing_cpu_ids = {cpu['id'] for cpu in data['components'].get('cpus', [])}
for cpu in new_cpus:
    if cpu['id'] not in existing_cpu_ids:
        data['components']['cpus'].append(cpu)

existing_gpu_ids = {gpu['id'] for gpu in data['components'].get('gpus', [])}
for gpu in new_gpus:
    if gpu['id'] not in existing_gpu_ids:
        data['components']['gpus'].append(gpu)

with open(data_path, 'w') as f:
    json.dump(data, f, indent=2)

print("Successfully added new items to seed_data.json")
