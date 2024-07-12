
# Package Installer

A Python class that automatically installs missing packages based on import statements in a script and generates a `requirements.txt` file using `pipreqs`. Please follow the steps below to install it on your personal computer.

## Features

- Automatically installs missing packages based on the imports in a specified script.
- Ensures that `pip` and `pipreqs` are installed.
- Generates a `requirements.txt` file for your project.

## Requirements

- Python 3.x

## Setup

To make the `PackageInstaller` class available globally on your computer, follow these steps:

1. **Download the Files**

2. **Install the Package Locally**:

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
