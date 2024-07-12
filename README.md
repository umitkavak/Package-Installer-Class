
# PackageInstaller

A Python class that automatically installs missing packages based on import statements in a specified script and generates a `requirements.txt` file using `pipreqs`.

## Features

- Automatically installs missing packages based on the imports in a specified script.
- Ensures that `pip` and `pipreqs` are installed.
- Generates a `requirements.txt` file for your project.

## Requirements

- Python 3.x

## Setup

To make the `PackageInstaller` class available globally on your computer, follow these steps:

1. **Create the Package Structure**:

    ```sh
    mkdir -p package_installer/package_installer
    touch package_installer/package_installer/__init__.py
    ```

2. **Create `installer.py`**:

    Create a file named `installer.py` inside the `package_installer/package_installer` directory with the following content:

    ```python
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
    ```

3. **Create `setup.py`**:

    Create a `setup.py` file in the root of the `package_installer` directory with the following content:

    ```python
    from setuptools import setup, find_packages

    setup(
        name='package_installer',
        version='0.1',
        packages=find_packages(),
        install_requires=[
            'pipreqs',
        ],
        entry_points={
            'console_scripts': [
                'install-packages=package_installer.installer:install_missing_packages',
            ],
        },
        description='A utility to automatically install missing packages and generate requirements.txt',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        author='Your Name',
        author_email='your.email@example.com',
        url='https://github.com/yourusername/package_installer',
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
        python_requires='>=3.6',
    )
    ```

4. **Create `LICENSE`**:

    Create a `LICENSE` file in the root of the `package_installer` directory with the following content:

    ```text
    MIT License

    Copyright (c) 2024 Umit Kavak

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    ```

5. **Create `README.md`**:

    Create a `README.md` file in the root of the `package_installer` directory with this content.

6. **Install the Package Locally**:

    Navigate to the root directory of your package and install it locally using `pip`:

    ```sh
    cd package_installer
    pip install .
    ```

## Using the Package

After installing the package, you can use it in any of your scripts by importing it and calling the function. For example:

```python
from package_installer.installer import install_missing_packages

install_missing_packages(__file__)

# Your script code starts here
import numpy as np
import pandas as pd
import sklearn
import matplotlib.pyplot as plt

# Example usage of the installed packages
print(np.array([1, 2, 3]))
print(pd.DataFrame({'A': [1, 2, 3]}))
```

## Contributing

Feel free to submit issues or pull requests if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
