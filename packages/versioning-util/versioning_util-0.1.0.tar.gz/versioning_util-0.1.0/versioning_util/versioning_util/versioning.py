import importlib.util as util
import os

class Version_Util:
    def __init__(self) -> None:
        self.version = None
        
def _get_version_from_setup(self):
    # Path to parent directory
    parent_dir = os.path.dirname(os.path.relpath(__file__))
    
    # Construct the path to setup.py
    setup_file = os.path.join(parent_dir, "setup.py")
    
    # Import version information using importlib
    spec = util.spec_from_file_location('setup', setup_file)
    module = util.module_from_spec(spec)
    util.execute(module)
    
    return module.__version__
    