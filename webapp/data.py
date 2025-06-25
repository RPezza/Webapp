import os
import django
import random
from datetime import date, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')  # Replace 'webapp' with your project name
django.setup()

from inventory.models import Asset

# Clear existing data (optional)
Asset.objects.all().delete()

# Sample data
asset_names = [
    "Leica 360", "RTC 360", "360 GoPro", "Insta360", "Spot", "Meta Quest 3", "Drone", "Sony Camera"
]
categories = ["Media Capture", "Visual", "Scanning", "Robotics"]

asset_data = [
    {"name": "Leica 360", "description": "High-precision 3D laser scanner for capturing spatial data.", "category": "Scanning"},
    {"name": "RTC 360", "description": "Rapid laser scanner for real-time 3D capture and registration.", "category": "Scanning"},
    {"name": "360 GoPro", "description": "Compact 360-degree camera for immersive video capture.", "category": "Media Capture"},
    {"name": "Insta360", "description": "Versatile 360 camera for action and VR content creation.", "category": "Media Capture"},
    {"name": "Spot", "description": "Agile robotic dog for inspection and data collection.", "category": "Robotics"},
    {"name": "Meta Quest 3", "description": "Advanced VR headset for immersive virtual experiences.", "category": "Visual"},
    {"name": "Drone", "description": "Aerial drone for capturing high-resolution images and videos.", "category": "Media Capture"},
    {"name": "Sony Camera", "description": "Professional-grade camera for photography and videography.", "category": "Media Capture"},
]

assets = []
for item in asset_data:
    asset = Asset.objects.create(
        name=item["name"],
        description=item["description"],
        category=item["category"],
        available=(True)
    )
    
    assets.append(asset)



