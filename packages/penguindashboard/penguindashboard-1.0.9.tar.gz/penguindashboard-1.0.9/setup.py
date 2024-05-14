from setuptools import setup, find_packages
import os

# Directory containing this file
this_directory = os.path.abspath(os.path.dirname(__file__))
# Text of the README file
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='penguindashboard',
    version='1.0.9',
    author='Aaron Feller, Phillip Woolley',
    author_email='aaronleefeller@gmail.com, prwoolley@utexas.edu',
    description='PEngUIN: Protein Engineering Using Independent Networks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AaronFeller/PEngUIN',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'penguin=penguindashboard.pipeline:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
)
