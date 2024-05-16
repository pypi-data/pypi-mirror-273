from setuptools import setup, find_packages

setup(
    name='annobee',
    version='0.3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'annobee=annobee.cli:main',
        ],
    },
    install_requires=[
        'numpy',
        'pandas',
        'tqdm',
        'dnspython',
        'pymongo',
        'requests',
        'six',
        'tzdata',
        'python-dateutil',
        'pytz',
        'pool',
    ],
    include_package_data=True,
    description='Annovar SDK for variant interpretation',
    url='https://github.com/variantAnnotation/annobee-sdk',  # Update with your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
