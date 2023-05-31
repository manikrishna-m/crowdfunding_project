from setuptools import setup,find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name = "CrowdFunds Raising Project",
    version = "0.0.1",
    author = "Mani Krishna",
    author_email = "mandepudi.mk@gmail.com",
    description = "Crowd Fund Raising Project",
    packages = find_packages(),
    install_requires = requirements
)