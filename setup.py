from setuptools import setup, find_packages

# Read the dependencies from requirements.txt
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

# Read the development dependencies from requirements-dev.txt
with open('requirements-dev.txt') as f:
    extras_require = {
        'dev': f.read().splitlines(),
    }

setup(
    name='evidently_dojo',
    version='1.0.0',
    packages=find_packages(),
    install_requires=install_requires,
    extras_require=extras_require,
)
