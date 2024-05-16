from setuptools import setup

def readme():
    with open('README.rst', 'r') as f:
        readme = f.read()
        return readme

setup(
    name='alltar',
    version='1.1',
    license='MIT',
    description='Tar Tool, written in Python, support on Linux and Windows',
    long_description=readme(),
    author='Kevin Alexander Krefting',
    author_email='pacspedd@outlook.com',
    scripts=['alltar']  # Note: Pass a list of script names
)

