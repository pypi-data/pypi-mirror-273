from setuptools import setup, find_packages

setup(
    name='personalization_profiles',
    version='0.1.4',
    packages=find_packages(),
    license='MIT',
    include_package_data=True,
    install_requires=[
        "numpy>= 1.20",
        "langchain"
    ],
    python_requires='>=3.9'
)