from setuptools import setup, find_packages

setup(
    name='Simplextep',
    version='0.1',
    packages=find_packages(),
    description='Simplex implementation with steps.',
    author='Keivan Jamali',
    author_email='K1Jamali01@gmail.com',
    url='https://github.com/KeivanJamali/simplex',
    install_requires=["numpy", "pandas", "tabulate", "matplotlib"],  # List any dependencies here
)