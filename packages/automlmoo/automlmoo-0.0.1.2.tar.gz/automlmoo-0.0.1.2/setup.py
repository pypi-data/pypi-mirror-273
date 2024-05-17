from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='automlmoo',
    packages=find_packages(include=['automlmoo']),
    version='0.0.1.2',
    description='A package for automatic modeling and optimize systems based on data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Yarens J. Cruz',
    install_requires=['auto-sklearn==0.15.0', 'pymoo==0.6.1.1', 'typeguard==4.2.1'],
    python_requires='>=3.7, <3.10',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    license='MIT',
)