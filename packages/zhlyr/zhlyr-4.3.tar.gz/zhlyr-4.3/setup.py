from setuptools import setup, find_packages
from Cython.Build import cythonize

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='zhlyr',
    version='4.3',
    packages=find_packages(),
    install_requires=['requests', 'shazamio', 'shazam', 'cython'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='Python library for music handling',
    author='Mtsky',
    author_email='secon2636@gmail.com',
    url='https://gaoc3.github.io/zhlyr/',
    license='MIT',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    keywords=['lyrics', 'music', 'shazam', 'serialize', 'serializer', 'recognize'],
    python_requires=">=3.9",
    package_data={"zhlyr":['serialize.pyx']}
)
