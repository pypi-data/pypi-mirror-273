from setuptools import setup, find_packages

setup(
    name='DPRED',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'biopython',
        'requests',
        'numpy',
        'logging'
    ],
    entry_points={
        'console_scripts': [
            'dpred=DPRED.main:main',
        ],
    },
    author='Daniele Ganci',
    author_email='daniele.ganci@studio.unibo.it',
    description='DPRED is a softwares package for HMM domain prediction and validation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dganci/DPRED',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)