import subprocess
import sys
import importlib
import re
import os

class PackageInstaller:
    """
    A class to automatically install missing packages based on import statements in a script.
    """
    def __init__(self, script_path):
        self.script_path = script_path
        self.package_mapping = {
            'sklearn': 'scikit-learn'
        }

    def install_pip(self):
        """
        Ensures that pip is installed.
        """
        try:
            subprocess.check_call([sys.executable, '-m', 'ensurepip'])
            print("pip is already installed.")
        except subprocess.CalledProcessError:
            print("pip is not installed. Installing pip...")
            try:
                subprocess.check_call([sys.executable, '-m', 'ensurepip', '--upgrade'])
                print("pip installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install pip: {e}")
                sys.exit(1)

    def install_and_import(self, package_name):
        """
        Attempts to import the specified package. If the package is not installed,
        it asks the user for confirmation to install the package using pip and then imports it.

        Args:
            package_name (str): The name of the package to import and install if necessary.
        """
        corrected_package_name = self.package_mapping.get(package_name, package_name)

        try:
            importlib.import_module(package_name)
            print(f"Package '{package_name}' is already installed.")
        except ImportError:
            response = input(f"Package '{package_name}' not found. Do you want to install '{corrected_package_name}'? (y/n): ").strip().lower()
            if response == 'y':
                print(f"Installing '{corrected_package_name}'...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", corrected_package_name])
                    print(f"Package '{corrected_package_name}' installed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to install package '{corrected_package_name}': {e}")
            else:
                print(f"Skipping installation of '{corrected_package_name}'.")

    def install_pipreqs(self):
        """
        Ensures that pipreqs is installed.
        """
        try:
            importlib.import_module('pipreqs')
            print("pipreqs is already installed.")
        except ImportError:
            response = input("pipreqs not found. Do you want to install pipreqs? (y/n): ").strip().lower()
            if response == 'y':
                print("Installing pipreqs...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "pipreqs"])
                    print("pipreqs installed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to install pipreqs: {e}")
            else:
                print("Skipping installation of pipreqs.")

    def run_pipreqs(self):
        """
        Runs pipreqs to generate a requirements.txt file.
        """
        print("Generating requirements.txt using pipreqs...")
        try:
            subprocess.check_call(["pipreqs", os.path.dirname(self.script_path), "--force"])
            print("requirements.txt generated successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to generate requirements.txt using pipreqs: {e}")

    def extract_imported_packages(self):
        """
        Extracts imported packages from the given script file.

        Returns:
            set: A set of package names that are imported in the script.
        """
        imported_packages = set()
        import_pattern = re.compile(r'^\s*(?:import|from)\s+([a-zA-Z0-9_\.]+)')

        with open(self.script_path, 'r') as file:
            for line in file:
                match = import_pattern.match(line)
                if match:
                    package = match.group(1).split('.')[0]
                    imported_packages.add(package)

        return imported_packages

    def ensure_script_dependencies(self):
        """
        Ensures all packages imported in the given script are installed.
        """
        self.install_pip()  # Ensure pip is installed before proceeding
        packages = self.extract_imported_packages()
        for package in packages:
            self.install_and_import(package)
        self.install_pipreqs()  # Ensure pipreqs is installed
        self.run_pipreqs()  # Generate requirements.txt

# Usage
def install_missing_packages(script_path):
    installer = PackageInstaller(script_path)
    installer.ensure_script_dependencies()
