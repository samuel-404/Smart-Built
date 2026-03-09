"""
Add 2019+ components with accurate 2026 Indian market pricing.
All fields match the exact structure in seed_data.json.
"""
import json, os

data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'seed_data.json')
with open(data_path, 'r') as f:
    data = json.load(f)

# ═══════════════════════════════════════════════════════════════════════════════
#  NEW GPUs — 2019 onwards, 2026 Indian prices
# ═══════════════════════════════════════════════════════════════════════════════
new_gpus = [
    # ── NVIDIA RTX 4000 (Ada Lovelace) — Missing from current data ──
    {"id": "gpu_040", "name": "NVIDIA GeForce RTX 4060", "brand": "NVIDIA", "vram": 8, "vram_type": "GDDR6", "tdp": 115, "length_mm": 240, "performance_score": 62, "price": 26999, "category": "mid-range", "ray_tracing": True, "dlss_version": 3, "architecture": "Ada Lovelace"},
    {"id": "gpu_041", "name": "NVIDIA GeForce RTX 4090", "brand": "NVIDIA", "vram": 24, "vram_type": "GDDR6X", "tdp": 450, "length_mm": 336, "performance_score": 100, "price": 174999, "category": "enthusiast", "ray_tracing": True, "dlss_version": 3, "architecture": "Ada Lovelace"},
    {"id": "gpu_042", "name": "NVIDIA GeForce RTX 4070 Ti SUPER", "brand": "NVIDIA", "vram": 16, "vram_type": "GDDR6X", "tdp": 285, "length_mm": 336, "performance_score": 88, "price": 74999, "category": "high-end", "ray_tracing": True, "dlss_version": 3, "architecture": "Ada Lovelace"},

    # ── NVIDIA RTX 3000 (Ampere, 2020-2022) ──
    {"id": "gpu_030", "name": "NVIDIA GeForce RTX 3060", "brand": "NVIDIA", "vram": 12, "vram_type": "GDDR6", "tdp": 170, "length_mm": 280, "performance_score": 52, "price": 24999, "category": "mid-range", "ray_tracing": True, "dlss_version": 2, "architecture": "Ampere"},
    {"id": "gpu_031", "name": "NVIDIA GeForce RTX 3060 Ti", "brand": "NVIDIA", "vram": 8, "vram_type": "GDDR6X", "tdp": 200, "length_mm": 300, "performance_score": 60, "price": 29999, "category": "mid-range", "ray_tracing": True, "dlss_version": 2, "architecture": "Ampere"},
    {"id": "gpu_032", "name": "NVIDIA GeForce RTX 3070", "brand": "NVIDIA", "vram": 8, "vram_type": "GDDR6X", "tdp": 220, "length_mm": 300, "performance_score": 66, "price": 36999, "category": "high-end", "ray_tracing": True, "dlss_version": 2, "architecture": "Ampere"},
    {"id": "gpu_033", "name": "NVIDIA GeForce RTX 3070 Ti", "brand": "NVIDIA", "vram": 8, "vram_type": "GDDR6X", "tdp": 290, "length_mm": 300, "performance_score": 70, "price": 42999, "category": "high-end", "ray_tracing": True, "dlss_version": 2, "architecture": "Ampere"},
    {"id": "gpu_034", "name": "NVIDIA GeForce RTX 3080", "brand": "NVIDIA", "vram": 10, "vram_type": "GDDR6X", "tdp": 320, "length_mm": 320, "performance_score": 78, "price": 52999, "category": "high-end", "ray_tracing": True, "dlss_version": 2, "architecture": "Ampere"},
    {"id": "gpu_035", "name": "NVIDIA GeForce RTX 3080 Ti", "brand": "NVIDIA", "vram": 12, "vram_type": "GDDR6X", "tdp": 350, "length_mm": 320, "performance_score": 82, "price": 62999, "category": "enthusiast", "ray_tracing": True, "dlss_version": 2, "architecture": "Ampere"},
    {"id": "gpu_036", "name": "NVIDIA GeForce RTX 3090", "brand": "NVIDIA", "vram": 24, "vram_type": "GDDR6X", "tdp": 350, "length_mm": 336, "performance_score": 85, "price": 94999, "category": "enthusiast", "ray_tracing": True, "dlss_version": 2, "architecture": "Ampere"},

    # ── NVIDIA GTX 1600 (Turing, 2019-2020) ──
    {"id": "gpu_050", "name": "NVIDIA GeForce GTX 1660 Super", "brand": "NVIDIA", "vram": 6, "vram_type": "GDDR6", "tdp": 125, "length_mm": 252, "performance_score": 35, "price": 17999, "category": "budget", "ray_tracing": False, "dlss_version": 0, "architecture": "Turing"},
    {"id": "gpu_051", "name": "NVIDIA GeForce GTX 1660 Ti", "brand": "NVIDIA", "vram": 6, "vram_type": "GDDR6", "tdp": 120, "length_mm": 252, "performance_score": 38, "price": 19999, "category": "budget", "ray_tracing": False, "dlss_version": 0, "architecture": "Turing"},

    # ── NVIDIA RTX 2000 (Turing, 2019) ──
    {"id": "gpu_052", "name": "NVIDIA GeForce RTX 2060", "brand": "NVIDIA", "vram": 6, "vram_type": "GDDR6", "tdp": 160, "length_mm": 268, "performance_score": 44, "price": 22999, "category": "mid-range", "ray_tracing": True, "dlss_version": 2, "architecture": "Turing"},
    {"id": "gpu_053", "name": "NVIDIA GeForce RTX 2070 Super", "brand": "NVIDIA", "vram": 8, "vram_type": "GDDR6", "tdp": 215, "length_mm": 281, "performance_score": 56, "price": 34999, "category": "high-end", "ray_tracing": True, "dlss_version": 2, "architecture": "Turing"},

    # ── AMD RX 6000 (RDNA 2, 2020-2022) ──
    {"id": "gpu_060", "name": "AMD Radeon RX 6600", "brand": "AMD", "vram": 8, "vram_type": "GDDR6", "tdp": 132, "length_mm": 238, "performance_score": 46, "price": 18999, "category": "budget", "ray_tracing": True, "dlss_version": 0, "architecture": "RDNA 2"},
    {"id": "gpu_061", "name": "AMD Radeon RX 6600 XT", "brand": "AMD", "vram": 8, "vram_type": "GDDR6", "tdp": 160, "length_mm": 260, "performance_score": 52, "price": 22999, "category": "mid-range", "ray_tracing": True, "dlss_version": 0, "architecture": "RDNA 2"},
    {"id": "gpu_062", "name": "AMD Radeon RX 6700 XT", "brand": "AMD", "vram": 12, "vram_type": "GDDR6", "tdp": 230, "length_mm": 267, "performance_score": 58, "price": 27999, "category": "mid-range", "ray_tracing": True, "dlss_version": 0, "architecture": "RDNA 2"},
    {"id": "gpu_063", "name": "AMD Radeon RX 6800 XT", "brand": "AMD", "vram": 16, "vram_type": "GDDR6", "tdp": 300, "length_mm": 267, "performance_score": 76, "price": 44999, "category": "high-end", "ray_tracing": True, "dlss_version": 0, "architecture": "RDNA 2"},
    {"id": "gpu_064", "name": "AMD Radeon RX 6900 XT", "brand": "AMD", "vram": 16, "vram_type": "GDDR6", "tdp": 300, "length_mm": 267, "performance_score": 80, "price": 54999, "category": "enthusiast", "ray_tracing": True, "dlss_version": 0, "architecture": "RDNA 2"},

    # ── AMD RX 9000 (RDNA 4, 2025-2026) ──
    {"id": "gpu_070", "name": "AMD Radeon RX 9070 XT", "brand": "AMD", "vram": 16, "vram_type": "GDDR6", "tdp": 300, "length_mm": 315, "performance_score": 84, "price": 57999, "category": "high-end", "ray_tracing": True, "dlss_version": 0, "architecture": "RDNA 4"},
    {"id": "gpu_071", "name": "AMD Radeon RX 9070", "brand": "AMD", "vram": 16, "vram_type": "GDDR6", "tdp": 250, "length_mm": 300, "performance_score": 76, "price": 49999, "category": "high-end", "ray_tracing": True, "dlss_version": 0, "architecture": "RDNA 4"},
    {"id": "gpu_072", "name": "AMD Radeon RX 9060 XT", "brand": "AMD", "vram": 8, "vram_type": "GDDR6", "tdp": 150, "length_mm": 260, "performance_score": 60, "price": 31999, "category": "mid-range", "ray_tracing": True, "dlss_version": 0, "architecture": "RDNA 4"},
]

# ═══════════════════════════════════════════════════════════════════════════════
#  NEW CPUs — 2019+, matching field structure
# ═══════════════════════════════════════════════════════════════════════════════
new_cpus = [
    # Intel 10th/11th Gen (LGA1200)
    {"id": "cpu_040", "name": "Intel Core i5-10400F", "brand": "Intel", "socket": "LGA1200", "cores": 6, "threads": 12, "base_clock": 2.9, "boost_clock": 4.3, "tdp": 65, "performance_score": 48, "gaming_score": 45, "price": 8499, "supported_ram": ["DDR4"], "integrated_graphics": False, "category": "budget"},
    {"id": "cpu_041", "name": "Intel Core i5-11400F", "brand": "Intel", "socket": "LGA1200", "cores": 6, "threads": 12, "base_clock": 2.6, "boost_clock": 4.4, "tdp": 65, "performance_score": 52, "gaming_score": 50, "price": 9999, "supported_ram": ["DDR4"], "integrated_graphics": False, "category": "budget"},

    # AMD Ryzen 3000 (Zen 2, AM4, 2019)
    {"id": "cpu_042", "name": "AMD Ryzen 5 3600", "brand": "AMD", "socket": "AM4", "cores": 6, "threads": 12, "base_clock": 3.6, "boost_clock": 4.2, "tdp": 65, "performance_score": 55, "gaming_score": 52, "price": 10999, "supported_ram": ["DDR4"], "integrated_graphics": False, "category": "budget"},
    {"id": "cpu_043", "name": "AMD Ryzen 7 3700X", "brand": "AMD", "socket": "AM4", "cores": 8, "threads": 16, "base_clock": 3.6, "boost_clock": 4.4, "tdp": 65, "performance_score": 68, "gaming_score": 60, "price": 15999, "supported_ram": ["DDR4"], "integrated_graphics": False, "category": "mid-range"},
    {"id": "cpu_044", "name": "AMD Ryzen 9 3900X", "brand": "AMD", "socket": "AM4", "cores": 12, "threads": 24, "base_clock": 3.8, "boost_clock": 4.6, "tdp": 105, "performance_score": 80, "gaming_score": 65, "price": 22999, "supported_ram": ["DDR4"], "integrated_graphics": False, "category": "high-end"},

    # AMD Ryzen 5000 (Zen 3, AM4) — missing ones
    {"id": "cpu_045", "name": "AMD Ryzen 5 5500", "brand": "AMD", "socket": "AM4", "cores": 6, "threads": 12, "base_clock": 3.6, "boost_clock": 4.2, "tdp": 65, "performance_score": 55, "gaming_score": 52, "price": 8999, "supported_ram": ["DDR4"], "integrated_graphics": False, "category": "budget"},
    {"id": "cpu_046", "name": "AMD Ryzen 7 5800X", "brand": "AMD", "socket": "AM4", "cores": 8, "threads": 16, "base_clock": 3.8, "boost_clock": 4.7, "tdp": 105, "performance_score": 78, "gaming_score": 76, "price": 19999, "supported_ram": ["DDR4"], "integrated_graphics": False, "category": "high-end"},
    {"id": "cpu_047", "name": "AMD Ryzen 9 5900X", "brand": "AMD", "socket": "AM4", "cores": 12, "threads": 24, "base_clock": 3.7, "boost_clock": 4.8, "tdp": 105, "performance_score": 85, "gaming_score": 78, "price": 24999, "supported_ram": ["DDR4"], "integrated_graphics": False, "category": "high-end"},

    # Intel 14th Gen — missing ones
    {"id": "cpu_048", "name": "Intel Core i5-14400F", "brand": "Intel", "socket": "LGA1700", "cores": 10, "threads": 16, "base_clock": 2.5, "boost_clock": 4.7, "tdp": 65, "performance_score": 74, "gaming_score": 70, "price": 16999, "supported_ram": ["DDR4", "DDR5"], "integrated_graphics": False, "category": "mid-range"},
    {"id": "cpu_049", "name": "Intel Core i7-14700KF", "brand": "Intel", "socket": "LGA1700", "cores": 20, "threads": 28, "base_clock": 3.4, "boost_clock": 5.6, "tdp": 125, "performance_score": 93, "gaming_score": 86, "price": 39999, "supported_ram": ["DDR4", "DDR5"], "integrated_graphics": False, "category": "high-end"},
]

# ═══════════════════════════════════════════════════════════════════════════════
#  NEW Motherboards — LGA1200 + more budget LGA1700/AM5
# ═══════════════════════════════════════════════════════════════════════════════
new_motherboards = [
    {"id": "mb_020", "name": "ASUS TUF Gaming B560M-PLUS WiFi", "brand": "ASUS", "socket": "LGA1200", "chipset": "B560", "form_factor": "Micro-ATX", "supported_ram": ["DDR4"], "ram_slots": 4, "max_ram_speed": 5000, "m2_slots": 2, "pcie_slots": 2, "price": 9999, "performance_score": 40},
    {"id": "mb_021", "name": "MSI MAG B560 Tomahawk WiFi", "brand": "MSI", "socket": "LGA1200", "chipset": "B560", "form_factor": "ATX", "supported_ram": ["DDR4"], "ram_slots": 4, "max_ram_speed": 5066, "m2_slots": 2, "pcie_slots": 2, "price": 11999, "performance_score": 42},
    {"id": "mb_022", "name": "MSI PRO B760M-A WiFi DDR4", "brand": "MSI", "socket": "LGA1700", "chipset": "B760", "form_factor": "Micro-ATX", "supported_ram": ["DDR4"], "ram_slots": 2, "max_ram_speed": 4800, "m2_slots": 2, "pcie_slots": 1, "price": 9499, "performance_score": 45},
    {"id": "mb_023", "name": "Gigabyte B650 AORUS Elite AX", "brand": "Gigabyte", "socket": "AM5", "chipset": "B650", "form_factor": "ATX", "supported_ram": ["DDR5"], "ram_slots": 4, "max_ram_speed": 6400, "m2_slots": 2, "pcie_slots": 2, "price": 22999, "performance_score": 72},
    {"id": "mb_024", "name": "MSI MPG B650 Carbon WiFi", "brand": "MSI", "socket": "AM5", "chipset": "B650", "form_factor": "ATX", "supported_ram": ["DDR5"], "ram_slots": 4, "max_ram_speed": 7200, "m2_slots": 3, "pcie_slots": 2, "price": 21999, "performance_score": 74},
]

# ═══════════════════════════════════════════════════════════════════════════════
#  ADD TO DATA
# ═══════════════════════════════════════════════════════════════════════════════
def add_items(category, items):
    existing = {c['id'] for c in data['components'][category]}
    added = 0
    for item in items:
        if item['id'] not in existing:
            data['components'][category].append(item)
            added += 1
    return added

total = 0
total += add_items('gpus', new_gpus)
total += add_items('cpus', new_cpus)
total += add_items('motherboards', new_motherboards)

with open(data_path, 'w') as f:
    json.dump(data, f, indent=2)

print(f"\nAdded {total} new components to seed_data.json")
for cat in data['components']:
    print(f"  {cat}: {len(data['components'][cat])}")
