import json
import os
from sheets import check_payment_proof, get_fan_rank

MEMORY_FILE = "fan_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

def update_fan_memory(user_id, text):
    memory = load_memory()
    if str(user_id) not in memory:
        memory[str(user_id)] = {"kinks": [], "spend": 0}
    memory[str(user_id)]["kinks"].append(text)
    save_memory(memory)

def get_fan_memory(user_id):
    memory = load_memory()
    fan_data = memory.get(str(user_id), {})
    return "\n".join(fan_data.get("kinks", []))

def add_spend(user_id, amount):
    memory = load_memory()
    if str(user_id) not in memory:
        memory[str(user_id)] = {"kinks": [], "spend": 0}
    memory[str(user_id)]["spend"] += amount
    save_memory(memory)

def get_spend(user_id):
    memory = load_memory()
    return memory.get(str(user_id), {}).get("spend", 0)

def get_fan_rank(user_id):
    return get_fan_rank(user_id)

def check_proof_sheet(user_id):
    return check_payment_proof(user_id)
