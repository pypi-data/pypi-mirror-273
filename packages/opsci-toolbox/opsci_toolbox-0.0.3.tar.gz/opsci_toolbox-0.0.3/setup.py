from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='opsci_toolbox',
    version='0.0.3',
    description="a complete toolbox",
    author='Erwan Le Nagard',
    author_email='erwan@opsci.ai',
    licence="MIT",
    packages=find_packages(),
    install_requires=requirements,  # Add any dependencies your library needs
    include_package_data=True,
    package_data={'': ['lexicons/*.csv']},  # Include all Python files in the lib directory
)