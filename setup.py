from setuptools import setup, find_packages
import os

# Read the contents of README file
current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='log-analyzer',
    version='1.1.0',
    author='selim',
    description='A Python script that analyzes log files to count total lines, ERROR and WARNING lines, and list error/warning messages',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zGaunna/LOG-ANALYZEr-.git',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'log-analyzer=log_analyzer.__main__:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)