from setuptools import setup, find_packages

setup(
    name='tse_motion',  # Looks like you need to correct this to tse_rating
    version='0.2.3',
    packages=find_packages(),  # This should automatically find tse_rating
    install_requires=[
        'torch',
        'monai',
        'nibabel',
        'torchvision'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'rate-motion=tse_rating.rate:main',  # Ensure the main function exists in artifact_rating.py
        ],
    },
    author='Jinghang Li',
    author_email='jinghang.li@pitt.edu',
    description='A package to rate motion artifacts in medical images.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jinghangli98/tse-rating',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
