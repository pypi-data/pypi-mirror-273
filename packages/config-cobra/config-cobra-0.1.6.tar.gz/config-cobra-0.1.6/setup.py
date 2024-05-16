from setuptools import setup, find_packages

# Parse requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='config-cobra',
    version='0.1.6',
    description='A simple yaml to database updater',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/JTSG1/configCobra',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'config-cobra=src.app:main',
        ],
    },
)