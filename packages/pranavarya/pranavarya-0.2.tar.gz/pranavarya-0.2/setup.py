from setuptools import setup, find_packages

setup(
    name='pranavarya',
    version='0.2',
    author='Pranav Arya',
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'pranavarya=pranavarya:hello',
        ],
    },
)