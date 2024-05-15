from setuptools import setup, find_packages

setup(
    name='personalization_profiles',
    version='0.1.2',
    packages=find_packages(),
    license='MIT',
    include_package_data=True,
    install_requires=[
        "numpy>= 1.20"
    ],
    python_requires='>=3.9'
)