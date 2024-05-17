import subprocess
import sys
import importlib

def install(package_name, import_name=None):
    """
    Ensure a package is installed and import it.

    :param package_name: Name of the package to ensure is installed.
    :param import_name: Name to use for importing the package (if different from package_name).
    :return: The imported package module.
    """
    try:
        # Try to import the package
        if import_name is None:
            import_name = package_name
        package = importlib.import_module(import_name)
        print(f"{package_name} is already installed.")
        return package
    except ImportError:
        # If not installed, install the package
        try:
            print(f"Installing {package_name}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"Successfully installed {package_name}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package_name}. Error: {e}")
            raise

        # Try to import again after installation
        package = importlib.import_module(import_name)
        return package
