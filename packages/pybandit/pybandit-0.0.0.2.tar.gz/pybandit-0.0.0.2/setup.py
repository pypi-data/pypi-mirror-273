from setuptools import find_packages, setup


# Function to read the list of requirements from requirements.txt
def read_requirements():
    with open("requirements.txt") as req:
        return req.read().splitlines()


setup(
    name="pybandit",
    version="0.0.0.2",
    license='Apache 2.0',
    description="Implementation of popular Multiarmed Bandit Algorithms",
    author='Tuhin Sharma',
    author_email='tuhinsharma121@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=("tests",)),
    install_requires=read_requirements(),
)
