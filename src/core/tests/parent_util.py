import sys
import os

def add_parent_dir_to_path():
    """Add the right directories to the Python path to make imports work.
    
    This does two important things:
    1. Adds the 'core' directory to the path so 'core.' imports work
    2. Adds the 'src' directory to the path so 'src.core.' imports work
    """
    # Add the src/core directory to path (for core. imports)
    core_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if core_path not in sys.path:
        sys.path.insert(0, core_path)
        
    # Add the src directory to path (for src.core. imports)
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if src_path not in sys.path:
        sys.path.insert(0, src_path)