from setuptools import setup, find_packages

setup(
    name = 'super_hello',
    version = '0.2',
    packages=find_packages(),
    install_requires=[],
    entry_points = {
        'console_scripts': [
            'super-hello = super_hello:hello'
        ]
    }
)