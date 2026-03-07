import json
import os

data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'seed_data.json')

with open(data_path, 'r') as f:
    data = json.load(f)

# Comprehensive list of profiles from image
new_profiles = {
    # Gaming & Streaming
    "gaming_esports": {"name": "Esports Gaming PC", "category": "Gaming & Streaming PC", "weights": {"gpu": 0.45, "cpu": 0.35, "ram": 0.1, "storage": 0.05, "motherboard": 0.03, "psu": 0.02}, "min_requirements": {"gpu_vram": 6, "ram_gb": 16, "cpu_cores": 6}},
    "gaming_casual": {"name": "Casual Gaming PC", "category": "Gaming & Streaming PC", "weights": {"gpu": 0.35, "cpu": 0.3, "ram": 0.15, "storage": 0.1, "motherboard": 0.05, "psu": 0.05}, "min_requirements": {"gpu_vram": 4, "ram_gb": 16, "cpu_cores": 4}},
    "gaming_aaa": {"name": "AAA Gaming PC", "category": "Gaming & Streaming PC", "weights": {"gpu": 0.5, "cpu": 0.2, "ram": 0.15, "storage": 0.05, "motherboard": 0.05, "psu": 0.05}, "min_requirements": {"gpu_vram": 8, "ram_gb": 16, "cpu_cores": 6}},
    
    # Streaming & Simulator
    "streaming_mobile": {"name": "Mobile Streaming PC", "category": "Streaming & Simulator PC", "weights": {"cpu": 0.4, "ram": 0.3, "gpu": 0.1, "storage": 0.1, "motherboard": 0.05, "psu": 0.05}, "min_requirements": {"ram_gb": 16, "cpu_cores": 6}},
    "streaming_pc": {"name": "PC Streaming PC", "category": "Streaming & Simulator PC", "weights": {"cpu": 0.35, "gpu": 0.35, "ram": 0.15, "storage": 0.05, "motherboard": 0.05, "psu": 0.05}, "min_requirements": {"ram_gb": 32, "cpu_cores": 8, "gpu_vram": 8}},
    "streaming_vr": {"name": "VR Gaming PC", "category": "Streaming & Simulator PC", "weights": {"gpu": 0.5, "cpu": 0.25, "ram": 0.1, "storage": 0.05, "motherboard": 0.05, "psu": 0.05}, "min_requirements": {"gpu_vram": 8, "ram_gb": 16, "cpu_cores": 6}},
    "simulator": {"name": "Simulator PC", "category": "Streaming & Simulator PC", "weights": {"cpu": 0.4, "gpu": 0.4, "ram": 0.1, "storage": 0.05, "motherboard": 0.03, "psu": 0.02}, "min_requirements": {"gpu_vram": 8, "ram_gb": 32, "cpu_cores": 8}},

    # Music Production
    "music_flstudio": {"name": "FL Studio PC", "category": "Music Production PCs", "weights": {"cpu": 0.5, "ram": 0.3, "storage": 0.1, "motherboard": 0.05, "gpu": 0.02, "psu": 0.03}, "min_requirements": {"ram_gb": 16, "cpu_cores": 6, "storage_gb": 1000}},
    "music_ableton": {"name": "Ableton PC", "category": "Music Production PCs", "weights": {"cpu": 0.5, "ram": 0.3, "storage": 0.1, "motherboard": 0.05, "gpu": 0.02, "psu": 0.03}, "min_requirements": {"ram_gb": 16, "cpu_cores": 6, "storage_gb": 1000}},

    # Video Editing
    "video_premiere": {"name": "Adobe Premiere Pro PC", "category": "Video Editing PC", "weights": {"cpu": 0.4, "gpu": 0.3, "ram": 0.2, "storage": 0.05, "motherboard": 0.03, "psu": 0.02}, "min_requirements": {"ram_gb": 32, "cpu_cores": 8, "gpu_vram": 6}},
    "video_davinci": {"name": "Davinci Resolve Studio PC", "category": "Video Editing PC", "weights": {"gpu": 0.45, "cpu": 0.25, "ram": 0.2, "storage": 0.05, "motherboard": 0.03, "psu": 0.02}, "min_requirements": {"ram_gb": 32, "cpu_cores": 8, "gpu_vram": 8}},

    # Layout & 3D Generalist
    "layout3d_maya": {"name": "Maya PC", "category": "Layout & 3D Generalist PC", "weights": {"cpu": 0.35, "gpu": 0.35, "ram": 0.2, "storage": 0.05, "motherboard": 0.02, "psu": 0.03}, "min_requirements": {"ram_gb": 32, "cpu_cores": 8, "gpu_vram": 8}},
    "layout3d_cinema4d": {"name": "Cinema 4D PC", "category": "Layout & 3D Generalist PC", "weights": {"cpu": 0.35, "gpu": 0.35, "ram": 0.2, "storage": 0.05, "motherboard": 0.02, "psu": 0.03}, "min_requirements": {"ram_gb": 32, "cpu_cores": 8, "gpu_vram": 8}},

    # Game Development
    "gamedev_unity": {"name": "Unity PC", "category": "Game Development PC", "weights": {"cpu": 0.35, "gpu": 0.3, "ram": 0.2, "storage": 0.1, "motherboard": 0.03, "psu": 0.02}, "min_requirements": {"ram_gb": 32, "cpu_cores": 6, "gpu_vram": 6}},
    "gamedev_ue5": {"name": "Unreal Engine 5 PC", "category": "Game Development PC", "weights": {"gpu": 0.4, "cpu": 0.3, "ram": 0.2, "storage": 0.05, "motherboard": 0.03, "psu": 0.02}, "min_requirements": {"ram_gb": 32, "cpu_cores": 8, "gpu_vram": 8}},
    "gamedev_blender": {"name": "Blender PC", "category": "Game Development PC", "weights": {"gpu": 0.45, "cpu": 0.25, "ram": 0.2, "storage": 0.05, "motherboard": 0.03, "psu": 0.02}, "min_requirements": {"ram_gb": 32, "cpu_cores": 8, "gpu_vram": 8}},

    # Architectural PC
    "arch_autocad": {"name": "AutoCAD PC", "category": "Architectural PC", "weights": {"cpu": 0.45, "ram": 0.25, "gpu": 0.15, "storage": 0.05, "motherboard": 0.05, "psu": 0.05}, "min_requirements": {"ram_gb": 16, "cpu_cores": 6}},
    "arch_sketchup": {"name": "Sketchup PC", "category": "Architectural PC", "weights": {"cpu": 0.45, "ram": 0.25, "gpu": 0.15, "storage": 0.05, "motherboard": 0.05, "psu": 0.05}, "min_requirements": {"ram_gb": 16, "cpu_cores": 6}},
    "arch_revit": {"name": "Revit PC", "category": "Architectural PC", "weights": {"cpu": 0.4, "ram": 0.3, "gpu": 0.2, "storage": 0.05, "motherboard": 0.03, "psu": 0.02}, "min_requirements": {"ram_gb": 32, "cpu_cores": 8, "gpu_vram": 4}},
    "arch_vray": {"name": "V-Ray PC", "category": "Architectural PC", "weights": {"gpu": 0.45, "cpu": 0.35, "ram": 0.15, "storage": 0.03, "motherboard": 0.01, "psu": 0.01}, "min_requirements": {"ram_gb": 32, "cpu_cores": 8, "gpu_vram": 8}},
    "arch_corona": {"name": "Corona Render PC", "category": "Architectural PC", "weights": {"cpu": 0.5, "ram": 0.25, "gpu": 0.15, "storage": 0.05, "motherboard": 0.03, "psu": 0.02}, "min_requirements": {"ram_gb": 32, "cpu_cores": 12}},
    "arch_octane": {"name": "Octane Render PC", "category": "Architectural PC", "weights": {"gpu": 0.55, "cpu": 0.2, "ram": 0.15, "storage": 0.05, "motherboard": 0.03, "psu": 0.02}, "min_requirements": {"ram_gb": 32, "cpu_cores": 8, "gpu_vram": 10}},

    # 3D Modelling
    "model3d_blender": {"name": "Blender PC", "category": "3D Modelling PC", "weights": {"gpu": 0.4, "cpu": 0.3, "ram": 0.2, "storage": 0.05, "motherboard": 0.03, "psu": 0.02}, "min_requirements": {"ram_gb": 32, "cpu_cores": 8, "gpu_vram": 8}},
    "model3d_lumion": {"name": "Lumion PC", "category": "3D Modelling PC", "weights": {"gpu": 0.5, "cpu": 0.25, "ram": 0.15, "storage": 0.05, "motherboard": 0.03, "psu": 0.02}, "min_requirements": {"ram_gb": 32, "cpu_cores": 8, "gpu_vram": 10}},
    "model3d_3dsmax": {"name": "3DsMax PC", "category": "3D Modelling PC", "weights": {"cpu": 0.35, "gpu": 0.35, "ram": 0.2, "storage": 0.05, "motherboard": 0.03, "psu": 0.02}, "min_requirements": {"ram_gb": 32, "cpu_cores": 8, "gpu_vram": 8}},
    "model3d_solidworks": {"name": "Solidworks PC", "category": "3D Modelling PC", "weights": {"cpu": 0.45, "ram": 0.25, "gpu": 0.15, "storage": 0.05, "motherboard": 0.05, "psu": 0.05}, "min_requirements": {"ram_gb": 16, "cpu_cores": 6}},

    # VFX Animation
    "vfx_nuke": {"name": "Nuke PC", "category": "VFX Animation PC", "weights": {"ram": 0.35, "cpu": 0.3, "storage": 0.15, "gpu": 0.1, "motherboard": 0.05, "psu": 0.05}, "min_requirements": {"ram_gb": 64, "cpu_cores": 8, "storage_gb": 1000}},
    "vfx_houdini": {"name": "Houdini PC", "category": "VFX Animation PC", "weights": {"ram": 0.35, "cpu": 0.35, "gpu": 0.15, "storage": 0.1, "motherboard": 0.03, "psu": 0.02}, "min_requirements": {"ram_gb": 64, "cpu_cores": 12, "gpu_vram": 8}},

    # Compositing 
    "comp_aftereffects": {"name": "Adobe After Effects PC", "category": "Compositing PC", "weights": {"ram": 0.4, "cpu": 0.35, "storage": 0.1, "gpu": 0.1, "motherboard": 0.03, "psu": 0.02}, "min_requirements": {"ram_gb": 64, "cpu_cores": 8, "storage_gb": 1000}},

    # Graphic Designing
    "graphic_photoshop": {"name": "Adobe Photoshop PC", "category": "Graphic Designing PCs", "weights": {"cpu": 0.4, "ram": 0.3, "storage": 0.1, "gpu": 0.1, "motherboard": 0.05, "psu": 0.05}, "min_requirements": {"ram_gb": 16, "cpu_cores": 6}},
    "graphic_illustrator": {"name": "Adobe Illustrator PC", "category": "Graphic Designing PCs", "weights": {"cpu": 0.4, "ram": 0.3, "storage": 0.1, "gpu": 0.1, "motherboard": 0.05, "psu": 0.05}, "min_requirements": {"ram_gb": 16, "cpu_cores": 6}},
    "graphic_corel": {"name": "Corel Draw Graphics Suite", "category": "Graphic Designing PCs", "weights": {"cpu": 0.4, "ram": 0.3, "storage": 0.1, "gpu": 0.1, "motherboard": 0.05, "psu": 0.05}, "min_requirements": {"ram_gb": 16, "cpu_cores": 4}},
    "graphic_figma": {"name": "Figma PC", "category": "Graphic Designing PCs", "weights": {"cpu": 0.3, "ram": 0.3, "storage": 0.1, "gpu": 0.1, "motherboard": 0.1, "psu": 0.1}, "min_requirements": {"ram_gb": 16, "cpu_cores": 4}},

    # Corporate Use Case
    "corp_ai": {"name": "AI & DeepLearning PC", "category": "Corporate Use Case", "weights": {"gpu": 0.55, "ram": 0.2, "cpu": 0.15, "storage": 0.05, "motherboard": 0.03, "psu": 0.02}, "min_requirements": {"ram_gb": 32, "cpu_cores": 8, "gpu_vram": 12}},
    "corp_coding": {"name": "Coding PC", "category": "Corporate Use Case", "weights": {"cpu": 0.4, "ram": 0.3, "storage": 0.1, "gpu": 0.05, "motherboard": 0.05, "psu": 0.1}, "min_requirements": {"ram_gb": 16, "cpu_cores": 6}},
    "corp_trading": {"name": "Trading PC", "category": "Corporate Use Case", "weights": {"cpu": 0.3, "ram": 0.3, "gpu": 0.15, "storage": 0.05, "motherboard": 0.1, "psu": 0.1}, "min_requirements": {"ram_gb": 16, "cpu_cores": 6}},
    "corp_office": {"name": "Home & Office PC", "category": "Corporate Use Case", "weights": {"cpu": 0.3, "ram": 0.25, "storage": 0.15, "gpu": 0.1, "motherboard": 0.1, "psu": 0.1}, "min_requirements": {"ram_gb": 8, "cpu_cores": 4}},
    "corp_signage": {"name": "Digital Signage PC", "category": "Corporate Use Case", "weights": {"cpu": 0.25, "ram": 0.2, "storage": 0.15, "gpu": 0.1, "motherboard": 0.15, "psu": 0.15}, "min_requirements": {"ram_gb": 8, "cpu_cores": 4}}
}

# Replace the old basic usage profiles with the new ones
data['usage_profiles'] = new_profiles

with open(data_path, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Added {len(new_profiles)} detailed usage profiles to seed_data.json.")
