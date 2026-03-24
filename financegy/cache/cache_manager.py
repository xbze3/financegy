import os, json, hashlib
from datetime import datetime, timedelta
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(SCRIPT_DIR, "cache")


def start_of_current_week(dt=None):
    """Returns Monday 00:00 of the current week."""
    dt = dt or datetime.now()
    monday = dt - timedelta(days=dt.weekday())
    return monday.replace(hour=0, minute=0, second=0, microsecond=0)


def make_cache_key(func_name, *args, **kwargs):
    """Create a unique hash for the given function call."""
    key_data = {"func": func_name, "args": args, "kwargs": kwargs}
    key_string = json.dumps(key_data, sort_keys=True, default=str)
    hashed = hashlib.md5(key_string.encode()).hexdigest()
    return f"{func_name}_{hashed}.json"


def load_cache(func_name, *args, **kwargs):
    """
    Load cache if it exists and is from the current week.
    If the requested cache file is stale, purge all stale cache files.
    If the requested file is corrupted, delete it.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)

    cache_file = make_cache_key(func_name, *args, **kwargs)
    cache_path = os.path.join(CACHE_DIR, cache_file)

    if not os.path.exists(cache_path):
        return None

    try:
        with open(cache_path, "r") as f:
            data = json.load(f)

        timestamp = datetime.fromisoformat(data["timestamp"])
        week_start = start_of_current_week()

        if timestamp < week_start:
            try:
                purge_old_cache_files()
            except Exception as e:
                print(f"Failed to purge stale cache files: {e}")
            return None

        return data["value"]

    except Exception:
        try:
            os.remove(cache_path)
        except Exception:
            pass
        return None


def save_cache(func_name, value, *args, **kwargs):
    """Save value to cache with current timestamp."""
    os.makedirs(CACHE_DIR, exist_ok=True)

    cache_file = make_cache_key(func_name, *args, **kwargs)
    cache_path = os.path.join(CACHE_DIR, cache_file)

    with open(cache_path, "w") as f:
        json.dump(
            {
                "timestamp": datetime.now().isoformat(),
                "value": value,
            },
            f,
        )


def clear_cache(silent: bool = False):
    """Completely clears the cache directory."""
    if not os.path.exists(CACHE_DIR):
        if not silent:
            print("No cache directory found.")
        return False

    try:
        shutil.rmtree(CACHE_DIR)
        if not silent:
            print("\nCache cleared successfully.")
        return True

    except Exception as e:
        print(f"Failed to clear cache: {e}")
        return False


def purge_old_cache_files():
    """
    Deletes any cache files not belonging to the current week.
    """
    if not os.path.exists(CACHE_DIR):
        return False

    week_start = start_of_current_week()
    deleted_any = False

    for filename in os.listdir(CACHE_DIR):
        path = os.path.join(CACHE_DIR, filename)

        if not os.path.isfile(path):
            continue

        try:
            with open(path, "r") as f:
                data = json.load(f)

            ts = datetime.fromisoformat(data["timestamp"])

            if ts < week_start:
                os.remove(path)
                deleted_any = True

        except Exception:
            try:
                os.remove(path)
                deleted_any = True
            except:
                pass

    return deleted_any
