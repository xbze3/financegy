import os, json, hashlib
from datetime import datetime, timedelta
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(SCRIPT_DIR, "cache")

def make_cache_key(func_name, *args, **kwargs):
    """Create a unique hash for the given function call."""

    key_data = {
        "func": func_name,
        "args": args,
        "kwargs": kwargs
    }

    key_string = json.dumps(key_data, sort_keys=True, default=str)
    hashed = hashlib.md5(key_string.encode()).hexdigest()

    return f"{func_name}_{hashed}.json"

def load_cache(func_name, *args, max_age_days=7, **kwargs):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = make_cache_key(func_name, *args, **kwargs)
    cache_path = os.path.join(CACHE_DIR, cache_file)

    if not os.path.exists(cache_path):
        return None

    with open(cache_path, "r") as f:
        data = json.load(f)

    timestamp = datetime.fromisoformat(data["timestamp"])
    if datetime.now() - timestamp > timedelta(days=max_age_days):
        return None

    return data["value"]

def save_cache(func_name, value, *args, **kwargs):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = make_cache_key(func_name, *args, **kwargs)
    cache_path = os.path.join(CACHE_DIR, cache_file)

    with open(cache_path, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "value": value
        }, f)

def clear_cache():
    """Completely clears the FinanceGY cache directory."""
    if not os.path.exists(CACHE_DIR):
        print("No cache directory found.")
        return False

    try:
        shutil.rmtree(CACHE_DIR)
        print("Cache cleared successfully.")
        return True
        
    except Exception as e:
        print(f"Failed to clear cache: {e}")