from setuptools import setup, find_packages

setup(
    name='Simplextep',
    version='0.1.5',
    packages=find_packages(),
    description='Simplex implementation with steps.',
    author='Keivan Jamali',
    author_email='K1Jamali01@gmail.com',
    url='https://github.com/KeivanJamali/simplextep',
    install_requires=["numpy", "pandas", "tabulate", "matplotlib"],
    license="MIT"
)