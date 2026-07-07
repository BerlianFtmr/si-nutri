import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDAR_FILE = os.path.join(BASE_DIR, 'data', 'standar_permenkes.json')

with open(STANDAR_FILE, 'r') as file:
    STANDAR_DATA = json.load(file)

def get_standar_gizi():
    return STANDAR_DATA