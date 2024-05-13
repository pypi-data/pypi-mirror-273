from setuptools import setup, find_packages

setup(
    name="cancer_simulation",
    version='0.7',
    packages=find_packages(),
    install_requires = [
        'pygame==2.5.2',
        'pygame-chart==1.0.0',
        'numpy==1.26.3',
        'PyYAML==6.0.1'
    ],
    entry_points = {
        'console_scripts': [
            "csim = src:main"
        ]
    }
)