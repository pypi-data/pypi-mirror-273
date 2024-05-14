from setuptools import setup, find_packages

setup(
    name='paradi',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0"
    ],
    python_requires='>=3.10',
    author='Julien Crambes',
    author_email='julien.crambes@gmail.com',
)
