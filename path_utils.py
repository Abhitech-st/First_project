import os
import sys

def get_app_path():
    """Get the application base path, works for both script and frozen exe"""
    if getattr(sys, 'frozen', False):
        # We are running in a PyInstaller bundle
        return os.path.dirname(sys.executable)
    else:
        # We are running in a normal Python environment
        return os.path.dirname(os.path.abspath(__file__))

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = get_app_path()
    return os.path.join(base_path, relative_path)

def ensure_dir(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
    return path