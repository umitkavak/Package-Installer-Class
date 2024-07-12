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
